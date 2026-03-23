import argparse
import base64
import mimetypes
import os
import sys
from pathlib import Path
 
try:
    import google.generativeai as genai
except ImportError:
    print("❌ google-generativeai 패키지가 필요합니다.")
    print("   pip install google-generativeai")
    sys.exit(1)
 
 
# ─────────────────────────────────────────────
# 설정
# ─────────────────────────────────────────────
 
DEFAULT_MODEL = "gemini-2.0-flash"
DEFAULT_SYSTEM = "당신은 유능하고 친절한 AI 어시스턴트입니다. 한국어로 대답해 주세요."
 
SUPPORTED_IMAGE_TYPES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
SUPPORTED_DOC_TYPES   = {".pdf", ".txt", ".md", ".csv", ".py", ".js", ".html", ".json"}
 
COMMANDS = """
────────────────────────────────────────
  명령어 목록
  /help        - 도움말 표시
  /clear       - 대화 기록 초기화
  /history     - 대화 기록 보기
  /system      - 시스템 프롬프트 변경
  /file <경로> - 파일 또는 이미지 첨부
  /model       - 현재 모델 확인
  /quit        - 종료
────────────────────────────────────────"""
 
 
# ─────────────────────────────────────────────
# 파일 처리
# ─────────────────────────────────────────────
 
def load_file(file_path: str) -> dict | None:
    """파일을 읽어 Gemini API 형식의 Part로 반환"""
    path = Path(file_path.strip())
 
    if not path.exists():
        print(f"  ❌ 파일을 찾을 수 없습니다: {path}")
        return None
 
    suffix = path.suffix.lower()
    mime_type, _ = mimetypes.guess_type(str(path))
 
    # 이미지
    if suffix in SUPPORTED_IMAGE_TYPES:
        mime_type = mime_type or "image/jpeg"
        with open(path, "rb") as f:
            data = base64.standard_b64encode(f.read()).decode("utf-8")
        print(f"  📷 이미지 첨부됨: {path.name}")
        return {"inline_data": {"mime_type": mime_type, "data": data}}
 
    # 문서 / 텍스트
    if suffix in SUPPORTED_DOC_TYPES:
        if suffix == ".pdf":
            mime_type = "application/pdf"
            with open(path, "rb") as f:
                data = base64.standard_b64encode(f.read()).decode("utf-8")
            print(f"  📄 PDF 첨부됨: {path.name}")
            return {"inline_data": {"mime_type": mime_type, "data": data}}
        else:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
            print(f"  📝 텍스트 파일 첨부됨: {path.name} ({len(text)} 글자)")
            return {"text": f"[파일: {path.name}]\n\n{text}"}
 
    print(f"  ⚠️  지원하지 않는 파일 형식입니다: {suffix}")
    print(f"     지원 이미지: {', '.join(SUPPORTED_IMAGE_TYPES)}")
    print(f"     지원 문서:   {', '.join(SUPPORTED_DOC_TYPES)}")
    return None
 
 
# ─────────────────────────────────────────────
# 챗봇 클래스
# ─────────────────────────────────────────────
 
class GeminiChatbot:
    def __init__(self, api_key: str, model_name: str, system_prompt: str):
        genai.configure(api_key=api_key)
 
        self.model_name   = model_name
        self.system_prompt = system_prompt
        self.history: list[dict] = []   # {"role": "user"|"model", "parts": [...]}
        self._init_model()
 
    def _init_model(self):
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=self.system_prompt,
        )
        self.chat = self.model.start_chat(history=self.history)
 
    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt
        self.history = []
        self._init_model()
        print(f"  ✅ 시스템 프롬프트 변경됨:\n     {prompt}")
 
    def clear_history(self):
        self.history = []
        self._init_model()
        print("  ✅ 대화 기록이 초기화되었습니다.")
 
    def show_history(self):
        if not self.chat.history:
            print("  (대화 기록 없음)")
            return
        print()
        for i, msg in enumerate(self.chat.history, 1):
            role = "👤 사용자" if msg.role == "user" else "🤖 Gemini"
            # parts를 텍스트로 요약
            texts = []
            for part in msg.parts:
                if hasattr(part, "text") and part.text:
                    texts.append(part.text[:80] + ("…" if len(part.text) > 80 else ""))
                else:
                    texts.append("[파일/이미지]")
            print(f"  [{i}] {role}: {'  |  '.join(texts)}")
        print()
 
    def send_message(self, user_text: str, extra_parts: list | None = None) -> None:
        """메시지 전송 및 스트리밍 출력"""
        parts: list = []
        if extra_parts:
            parts.extend(extra_parts)
        parts.append(user_text)
 
        print("\n🤖 Gemini: ", end="", flush=True)
        try:
            response = self.chat.send_message(parts, stream=True)
            for chunk in response:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
            print("\n")
        except Exception as e:
            print(f"\n  ❌ 오류 발생: {e}\n")
 
 
# ─────────────────────────────────────────────
# 메인 루프
# ─────────────────────────────────────────────
 
def main():
    parser = argparse.ArgumentParser(description="Gemini API 챗봇")
    parser.add_argument("--api-key", help="Gemini API 키 (없으면 GEMINI_API_KEY 환경변수 사용)")
    parser.add_argument("--model",   default=DEFAULT_MODEL, help=f"사용할 모델 (기본: {DEFAULT_MODEL})")
    parser.add_argument("--system",  default=DEFAULT_SYSTEM, help="시스템 프롬프트")
    args = parser.parse_args()
 
    # API 키 확인
    api_key = args.api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Gemini API 키가 필요합니다.")
        print("   방법 1: --api-key YOUR_KEY 옵션 사용")
        print("   방법 2: GEMINI_API_KEY 환경변수 설정")
        print("   API 키 발급: https://aistudio.google.com/apikey")
        sys.exit(1)
 
    # 챗봇 초기화
    try:
        bot = GeminiChatbot(api_key, args.model, args.system)
    except Exception as e:
        print(f"❌ 초기화 실패: {e}")
        sys.exit(1)
 
    print("=" * 48)
    print("  🤖 Gemini 챗봇")
    print(f"  모델: {args.model}")
    print(f"  시스템: {args.system[:50]}{'…' if len(args.system) > 50 else ''}")
    print("  '/help' 입력 시 명령어 목록 표시")
    print("=" * 48)
 
    pending_files: list[dict] = []   # 다음 메시지에 첨부할 파일 parts
 
    while True:
        try:
            user_input = input("👤 나: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 종료합니다.")
            break
 
        if not user_input:
            continue
 
        # ── 명령어 처리 ──────────────────────────
        if user_input.startswith("/"):
            cmd_parts = user_input.split(maxsplit=1)
            cmd = cmd_parts[0].lower()
            arg = cmd_parts[1] if len(cmd_parts) > 1 else ""
 
            if cmd == "/quit":
                print("👋 종료합니다.")
                break
 
            elif cmd == "/help":
                print(COMMANDS)
 
            elif cmd == "/clear":
                bot.clear_history()
                pending_files.clear()
 
            elif cmd == "/history":
                bot.show_history()
 
            elif cmd == "/model":
                print(f"  현재 모델: {bot.model_name}")
 
            elif cmd == "/system":
                if arg:
                    bot.set_system_prompt(arg)
                else:
                    print(f"  현재 시스템 프롬프트: {bot.system_prompt}")
                    new_prompt = input("  새 프롬프트 입력 (빈 칸이면 취소): ").strip()
                    if new_prompt:
                        bot.set_system_prompt(new_prompt)
 
            elif cmd == "/file":
                if not arg:
                    arg = input("  파일 경로 입력: ").strip()
                if arg:
                    part = load_file(arg)
                    if part:
                        pending_files.append(part)
                        print(f"  ✅ 파일이 다음 메시지에 첨부됩니다. (현재 {len(pending_files)}개)")
 
            else:
                print(f"  ❓ 알 수 없는 명령어: {cmd}  ('/help' 참고)")
 
        # ── 일반 메시지 전송 ─────────────────────
        else:
            bot.send_message(user_input, extra_parts=pending_files if pending_files else None)
            pending_files.clear()
 
 
if __name__ == "__main__":
    main()