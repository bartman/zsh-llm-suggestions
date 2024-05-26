#!/usr/bin/env python3

import sys
import os
import subprocess

def highlight_explanation(explanation):
  try:
    import pygments
    from pygments.lexers import MarkdownLexer
    from pygments.formatters import TerminalFormatter
    return pygments.highlight(explanation, MarkdownLexer(), TerminalFormatter(style='material'))
  except ImportError:
    return explanation

def setup_ollama(name, file):
  command = ["ollama", "create", name, "--file", file]
  result = subprocess.run(command, capture_output=True, text=True)
  if result.returncode == 0:
    print(f"Successfully generated {name} ollma profile.")
    return True

  print(f"ERROR: Failed to setup {name} ollama profile.", file=sys.stderr)
  print(result.stderr, file=sys.stderr)
  sys.exit(1)

def run_ollama(model, prompt):
  command = ["ollama", "run", model, prompt]
  result = subprocess.run(command, capture_output=True, text=True)
  if result.returncode == 0:
    return True, result.stdout
  return False, result.stderr

def main():
  mode = sys.argv[1] if len(sys.argv)>1 else None
  if mode == 'setup':
    setup_ollama("zsh-llm-suggesions-generate", "zsh-llm-suggestions-ollama.generate.modelfile")
    setup_ollama("zsh-llm-suggesions-explain", "zsh-llm-suggestions-ollama.explain.modelfile")
    return

  elif mode == 'generate':
    model = os.environ.get('ZSH_OLLAMA_GENERATE_MODEL') or 'zsh-llm-suggesions-generate'

  elif mode == 'explain':
    model = os.environ.get('ZSH_OLLAMA_EXPLAIN_MODEL') or 'zsh-llm-suggesions-explain'

  else:
    print("ERROR: something went wrong in zsh-llm-suggestions, please report a bug. Got unknown mode: " + str(mode), file=sys.stderr)
    sys.exit(1)

  prompt = sys.stdin.read().strip()
  ok, result = run_ollama(model, prompt)
  if not ok:
    print("ERROR: something went wrong:\n" + result.strip(), file=sys.stderr)
    sys.exit(1)

  elif mode == 'generate':
    result = result.replace('```zsh', '').replace('```', '').strip()
    print(result)

  elif mode == 'explain':
    print(highlight_explanation(result))

if __name__ == '__main__':
  main()
