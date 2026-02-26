# Contributing to NanoClaw

## How to add a skill

1. Create a new file: `skills/your_skill_name.py`
2. Inherit from `BaseSkill`
3. Fill in `name`, `description`, `args_schema`
4. Implement `run()`
5. Test it: `python main.py -m "use your_skill_name"`

## Code style

- Keep skills self-contained (all imports inside the file)
- Handle errors gracefully — return error strings, don't raise
- `run()` must always return a string
- Keep descriptions clear, as they are shown directly to the LLM

## Pull Request checklist

- [ ] Skill works in isolation
- [ ] Error cases handled
- [ ] No hardcoded API keys
- [ ] `args_schema` documents all arguments