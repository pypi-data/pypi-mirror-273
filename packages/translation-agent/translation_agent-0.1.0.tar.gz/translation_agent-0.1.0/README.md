# Translation Agent: Agentic translation using reflection workflow

Translation Agent is a Python-based project that leverages an agentic workflow for machine translation tasks. The repository contains code that utilizes the power of Reflection to enhance the translation process and improve the quality of the generated translations.
## Features

- Agentic Workflow: Translation Agent employs an agentic workflow, which allows for a more intelligent and context-aware approach to machine translation. By incorporating Reflection, the system can analyze and understand the source text more effectively, resulting in more accurate and fluent translations.
- Reflection-based Translation: The core of Translation Agent lies in its use of Reflection, a technique that enables the system to introspect and reason about its own translation process. By reflecting on the intermediate steps and considering the context and meaning of the source text, the system can make informed decisions and generate translations that better capture the intended meaning.
- Language Support: Translation Agent supports a wide range of languages, making it a versatile tool for translating text across different linguistic boundaries. Whether you need to translate between commonly spoken languages or handle less-resourced language pairs, Translation Agent has you covered.
- Customizable Models: The repository provides a flexible framework that allows you to customize and fine-tune the translation models according to your specific requirements. You can experiment with different architectures, training data, and hyperparameters to optimize the translation quality for your use case.
- Easy Integration: Translation Agent is designed to be easily integrated into existing projects and workflows. With a simple and intuitive API, you can seamlessly incorporate machine translation capabilities into your applications, websites, or data pipelines.


## Getting Started

To get started with Translation Agent, follow these steps:

### Installation:

```bash
pip install translation-agent
```


### Usage:

```python
import translation_agent as ta

source_lang, target_lang = "English", "Spanish"

translation = ta.translate(source_lang, target_lang, source_text)
```

## Benchmarks:

spBLEU

|           | GPT-4(agents) | Google Translate | DeepL | NLLB-200 |
|-----------|---------------|------------------|-------|----------|
| en -> spa |               | 35.31            | 33.48 |          |
| en -> deu |               | 48.33            | 50.23 |          |
|           |               |                  |       |          |


## Contributing

We welcome contributions from the community to enhance Translation Agent and expand its capabilities. If you have any ideas, bug fixes, or improvements, please submit a pull request or open an issue on the GitHub repository. Make sure to follow the contribution guidelines outlined in `CONTRIBUTING.md`.

## License

Translation Agent is released under the **MIT License**. You are free to use, modify, and distribute the code for both commercial and non-commercial purposes.
