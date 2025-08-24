import os
from typing import Dict, List, Any
from .workflow import MemeStockWorkflow
from .feedback import record_feedback
from ..utils.logging_setup import get_logger
from ..utils.config import get_settings

# Proper Portia SDK import handling
try:
    from portia import (
        Portia, Config, LLMProvider, LLMModel, 
        ToolRegistry, SearchTool, WeatherTool, CrawlTool, ExtractTool, MapTool
    )
    PORTIA_AVAILABLE = True
except ImportError:
    PORTIA_AVAILABLE = False

logger = get_logger(__name__)

class PortiaMemeAgent:
    def __init__(self):
        self.workflow = MemeStockWorkflow()
        self._history: Dict[str, List[Dict]] = {}
        self._portia_client = None
        self._cloud_tools_available = False
        self._tool_count = 0
        
        if PORTIA_AVAILABLE:
            self._initialize_portia()
        else:
            logger.warning("Portia SDK not available - running in basic mode")

    def _initialize_portia(self):
        """Initialize Portia client with Google Gemini LLM (graceful degradation)."""
        settings = get_settings()
        api_key = settings.portia_api_key
        google_api_key = os.getenv('GOOGLE_API_KEY')

        if not api_key:
            logger.warning("PORTIA_API_KEY not set; enhanced analysis unavailable")
            return
        if not google_api_key:
            logger.warning("GOOGLE_API_KEY not set; Gemini features limited")

        try:
            # Create Portia config with Google Gemini LLM
            cfg = Config(
                portia_api_key=api_key,
                google_api_key=google_api_key,
                llm_provider=LLMProvider.GOOGLE,
            )
            
            # Build local tool set first (avoid automatic cloud fetch to prevent 401)
            local_tools = [
                SearchTool(),      # Web search capabilities
                WeatherTool(),     # Weather data for market analysis
                CrawlTool(),       # Web crawling for news/data
                ExtractTool(),     # Data extraction
                MapTool(),         # Data transformation
            ]
            local_registry = ToolRegistry(local_tools)
            
            try:
                self._portia_client = Portia(config=cfg, tools=local_registry)
                self._tool_count = len(local_tools)
                logger.info(f"Portia initialized with Google Gemini + {self._tool_count} local tools")
            except Exception as e:
                if '401' in str(e) or 'Unauthorized' in str(e):
                    logger.warning("Portia cloud auth failed (401). Using local tools only. Verify API key.")
                else:
                    logger.warning(f"Portia core init failed: {e}")
                self._portia_client = None
                return

        except Exception as outer:
            logger.warning(f"Portia initialization failed (graceful fallback to basic mode): {outer}")
            self._portia_client = None

    def get_portia_status(self) -> Dict[str, Any]:
        """Get detailed Portia integration status"""
        status = {
            'portia_available': PORTIA_AVAILABLE,
            'client_initialized': self._portia_client is not None,
            'cloud_tools_available': self._cloud_tools_available,
            'tool_count': self._tool_count,
            'google_gemini_ready': self._portia_client is not None,
            'portia_api_configured': bool(get_settings().portia_api_key)
        }
        if self._portia_client is None and bool(get_settings().portia_api_key):
            status['warning'] = 'Portia cloud auth failed; operating with basic workflow only.'
        return status

    def _append_history(self, conversation_id: str, role: str, content: str):
        self._history.setdefault(conversation_id, []).append({"role": role, "content": content})
        # Optional trim
        if len(self._history[conversation_id]) > 50:
            self._history[conversation_id] = self._history[conversation_id][-50:]

    def handle_query(self, conversation_id: str, text: str) -> Dict:
        self._append_history(conversation_id, "user", text)
        lower = text.lower().strip()

        if lower.startswith("feedback"):
            parts = lower.split(":", 2)
            rating = parts[1] if len(parts) > 1 else "none"
            notes = parts[2] if len(parts) > 2 else ""
            record_feedback(conversation_id, rating, notes)
            response = {"response": "Feedback appreciated!"}
            self._append_history(conversation_id, "assistant", response["response"])
            self._send_to_portia(conversation_id, text, response["response"], meta={"type": "feedback"})
            return response

        if any(k in lower for k in ["explain", "methodology", "how"]):
            msg = "Ask about a ticker like 'TSLA memes?' to get a playful sentiment+memes analysis."
            self._append_history(conversation_id, "assistant", msg)
            self._send_to_portia(conversation_id, text, msg, meta={"type": "help"})
            return {"response": msg}

        words = [w.strip("$?!. ,") for w in lower.split()]
        ticker = None
        for w in words:
            if w.isalpha() and 2 < len(w) <= 5:
                ticker = w.upper()
                break
        if not ticker:
            msg = "Please specify a ticker (e.g., 'GME memes?')."
            self._append_history(conversation_id, "assistant", msg)
            self._send_to_portia(conversation_id, text, msg, meta={"type": "no_ticker"})
            return {"response": msg}

        # Enhanced analysis with Portia AI if available
        if self._portia_client:
            try:
                enhanced_result = self._analyze_with_portia_ai(ticker, conversation_id)
                if enhanced_result:
                    message = enhanced_result['message']
                    self._append_history(conversation_id, "assistant", message)
                    self._send_to_portia(conversation_id, text, message, meta={"type": "enhanced_analysis", "ticker": ticker, **enhanced_result.get('prediction', {})})
                    return {"response": message, "details": enhanced_result}
            except Exception as e:
                logger.warning(f"Enhanced analysis failed, falling back to basic: {e}")

        # Fallback to basic analysis
        result = self.workflow.run(ticker)
        message = result['message']
        self._append_history(conversation_id, "assistant", message)
        self._send_to_portia(conversation_id, text, message, meta={"type": "analysis", "ticker": ticker, **result.get('prediction', {})})
        return {"response": message, "details": result}

    def _analyze_with_portia_ai(self, ticker: str, user_id: str) -> Dict[str, Any]:
        """Enhanced analysis using Portia AI with Google Gemini"""
        if not self._portia_client:
            return None
        
        try:
            # Get basic analysis first
            basic_result = self.workflow.run(ticker)
            
            # Create enhanced analysis prompt for Google Gemini
            analysis_prompt = f"""
            Enhance this meme stock analysis for {ticker} using the provided data:
            
            Basic Analysis: {basic_result}
            
            Provide an enhanced analysis that:
            1. Summarizes the key findings in a fun, engaging way
            2. Highlights the most important meme potential indicators
            3. Adds context about recent market trends for this stock
            4. Gives a witty, memorable conclusion
            5. Maintains the humorous tone while being informative
            
            Format as a conversational response that's both educational and entertaining.
            """
            
            # Use Portia's run method for AI analysis
            portia_result = self._portia_client.run(analysis_prompt)
            
            # Combine results
            enhanced_result = {
                **basic_result,
                "ai_enhanced": True,
                "enhanced_message": portia_result.output if hasattr(portia_result, 'output') else str(portia_result),
                "portia_analysis": True,
                "tool_count_used": self._tool_count
            }
            
            # Use the AI-enhanced message if available
            if hasattr(portia_result, 'output') and portia_result.output:
                enhanced_result['message'] = portia_result.output
            
            return enhanced_result
            
        except Exception as e:
            logger.warning(f"Portia AI analysis failed for {ticker}: {e}")
            return None

    def _send_to_portia(self, conversation_id: str, user_text: str, assistant_text: str, meta: Dict):
        """Log interaction to Portia for learning and improvement"""
        if not self._portia_client:
            return
        try:
            # Use Portia to analyze and log the conversation for continuous improvement
            log_prompt = f"""
            Log this interaction for analysis:
            User: {user_text}
            Assistant: {assistant_text}
            Metadata: {meta}
            
            This helps improve future stock analysis accuracy.
            """
            
            # Run async to avoid blocking
            try:
                self._portia_client.run(log_prompt)
            except Exception:
                pass  # Don't block on logging failures
                
        except Exception as e:
            logger.debug(f"Portia interaction logging failed: {e}")
