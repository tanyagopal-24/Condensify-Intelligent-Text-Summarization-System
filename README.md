# Condensify-Intelligent-Text-Summarization-System
Condensify is an unsupervised extractive text summarization system that converts long-form documents into concise, meaningful summaries using Natural Language Processing techniques.
The system leverages TF-IDF vectorization and sentence ranking to identify the most information-rich sentences.

It supports:
 1. TXT files
 2. PDF documents
 3. Word (.docx) files
 4. Manual text input

🧠 Core Features
 * Multi-format file support (TXT, PDF, DOCX)
 * NLP-based sentence tokenization (NLTK)
 * TF-IDF vectorization
 * Sentence importance scoring
 * Word comparison visualization
 * Reduction percentage metrics
 * Downloadable summaries
 * Modern interactive UI (Streamlit)

🏗 System Architecture
1. Document Upload / Text Input
2. Sentence Tokenization (NLTK)
3. TF-IDF Vectorization
4. Sentence Scoring (Sum of TF-IDF weights)
5. Top-N Sentence Selection
6. Summary Generation
7. Visualization & Metrics Display

⚙️ How the Model Works (Technical Explanation)

-Condensify uses unsupervised extractive summarization:
1. Sentences are tokenized using NLTK.
2. Each sentence is converted into a TF-IDF vector.
3. Sentence importance is computed using aggregate TF-IDF scores.
4. Top N highest scoring sentences are selected.
5. Original order is preserved for coherence.

-Unlike abstractive models (like transformers), this method ensures:
* Fast performance
* No training required
* Deterministic outputs
* Lightweight deployment

🛠 Tech Stack
* Frontend: Streamlit
* NLP: NLTK
* ML Technique: TF-IDF (Scikit-learn)
* Visualization: Matplotlib
* PDF Parsing: PyPDF2
* DOCX Parsing: python-docx
* Development Environment: Visual Studio Code (VS Code)
* Language: Python


