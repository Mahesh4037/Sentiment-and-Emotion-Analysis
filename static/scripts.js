document.addEventListener("DOMContentLoaded", function () {
    // Element Selectors
    const elements = {
        submitButton: document.getElementById("submit-feedback"),
        startRecordingButton: document.getElementById("start-recording"),
        resultElement: document.getElementById("result"),
        resultContainer: document.getElementById("result-container"),
        graphsContainer: document.getElementById("graphs-container"),
        translatedFeedbackElement: document.getElementById("translated-feedback"),
        textareaElement: document.getElementById("feedback"),
        dropdownButton: document.querySelector(".dropdown-button"),
        dropdownContainer: document.querySelector(".dropdown-container"),
        languageLinks: document.querySelectorAll(".language-grid a"),
        searchBar: document.querySelector(".search-bar"),
        speakerTextareaButton: document.getElementById("speaker-textarea"),
        speakerFeedbackButton: document.getElementById("speaker-feedback"),
        copyTextareaButton: document.getElementById("copy-textarea"), // Corrected ID from original code
        copyFeedbackButton: document.getElementById("copy-feedback")
    };

    let selectedLanguage = "en"; // Default language is English
    let isSpeaking = false;      // State to track if speech is active

    // Web Speech API for voice input
    // Ensure the API is available before using it
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.onresult = (event) => {
            elements.textareaElement.value = event.results[0][0].transcript;
        };
        recognition.onerror = (event) => alert("Speech recognition error: " + event.error);
        elements.startRecordingButton.addEventListener("click", () => recognition.start());
    } else {
        elements.startRecordingButton.style.display = 'none'; // Hide button if not supported
    }

    // Event Listeners
    elements.submitButton.addEventListener("click", async (event) => {
        event.preventDefault();
        const feedback = elements.textareaElement.value.trim();

        if (!feedback) return alert("Please enter feedback.");

        try {
            // Translate feedback if necessary
            const translatedFeedback = selectedLanguage !== "en" ? await translateText(feedback) : feedback;

            // Analyze feedback
            const analysisData = await analyzeFeedback(feedback);
            displayAnalysisResults(analysisData, translatedFeedback);
            generateCharts(analysisData.probabilities);

        } catch (error) {
            console.error("Error during submit:", error);
            alert("An error occurred while processing your feedback.");
        }
    });

    elements.languageLinks.forEach((item) => {
        item.addEventListener("click", (e) => {
            e.preventDefault();
            selectedLanguage = item.getAttribute("data-lang");
            elements.dropdownButton.textContent = `Translate to: ${item.textContent}`;
            elements.dropdownContainer.classList.remove("open");
        });
    });

    // Language Search Filtering
    document.querySelector(".search-bar").addEventListener("input", function (e) {
        const searchTerm = e.target.value.toLowerCase();
        document.querySelectorAll(".language-grid a").forEach((item) => {
            const language = item.textContent.toLowerCase();
            item.style.display = language.includes(searchTerm) ? "block" : "none";
        });
    });

    elements.dropdownButton.addEventListener("click", () => {
        elements.dropdownContainer.classList.toggle("open");
    });

    // Add event listeners to speaker buttons
    elements.speakerTextareaButton.addEventListener("click", () => readTextAloud("feedback"));
    elements.speakerFeedbackButton.addEventListener("click", () => readTextAloud("translated-feedback"));

    // Add event listeners to copy buttons
    elements.copyTextareaButton.addEventListener("click", () => copyToClipboard("feedback"));
    elements.copyFeedbackButton.addEventListener("click", () => copyToClipboard("translated-feedback"));


    // =========================================================================
    // API and Helper Functions
    // =========================================================================

    async function translateText(text) {
        try {
            const response = await fetch("/translate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text, language: selectedLanguage }),
            });
            if (!response.ok) throw new Error("Translation request failed.");
            return (await response.json()).translated_text;
        } catch (error) {
            console.error("Error translating text:", error);
            return text; // Return original text if translation fails
        }
    }

    async function analyzeFeedback(feedback) {
        try {
            const response = await fetch("/analyze-feedback", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ feedback }),
            });
            if (!response.ok) throw new Error("Feedback analysis request failed.");
            return await response.json();
        } catch (error) {
            console.error("Error analyzing feedback:", error);
            throw error;
        }
    }

    // =========================================================================
    // Chart Generation
    // =========================================================================
    async function generateCharts(probabilities) {
        await generateProbabilityBarChart(probabilities);
        await generateEmotionPieChart(probabilities);
        // Ensure charts are responsive
        window.onresize = () => {
            Plotly.Plots.resize(document.getElementById("probability-chart"));
            Plotly.Plots.resize(document.getElementById("emotion-pie-chart"));
        };
    }

    async function generateProbabilityBarChart(probabilities) {
        const labels = Object.keys(probabilities);
        const values = Object.values(probabilities).map(value => parseFloat(value.toFixed(2)));

        const data = [{
            x: labels,
            y: values,
            type: "bar",
            marker: { color: "rgba(58, 71, 80, 0.8)" },
        }];
        const layout = {
            title: "Prediction Probabilities",
            xaxis: { title: "Emotions", tickangle: -45 },
            yaxis: { title: "Probability", range: [0, 1] },
            margin: { t: 50, b: 120, l: 70, r: 50 },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: {
                color: '#22333B'
            }
        };
        Plotly.newPlot("probability-chart", data, layout, {responsive: true});
    }

    async function generateEmotionPieChart(probabilities) {
        const labels = Object.keys(probabilities);
        const values = Object.values(probabilities).map(value => parseFloat(value.toFixed(2)));

        const data = [{
            labels: labels,
            values: values,
            type: "pie",
            hole: 0.4,
            textinfo: "none",
            hoverinfo: "label+value",
        }];
        const layout = {
            title: "Emotion Distribution",
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: {
                color: '#22333B'
            }
        };
        Plotly.newPlot("emotion-pie-chart", data, layout, {responsive: true});
    }

    // =========================================================================
    // THE FIX: Corrected Text-to-Speech Function
    // =========================================================================
    /**
     * Reads text from a given element ID aloud.
     * Includes fixes for common browser speech synthesis issues.
     * @param {string} elementId - The ID of the element containing the text.
     */
    function readTextAloud(elementId) {
        const text = document.getElementById(elementId).value;
        if (!text || text.trim() === "") {
            alert("There is no text to read.");
            return;
        }

        // If it's already speaking, stop it.
        if (isSpeaking) {
            speechSynthesis.cancel();
            isSpeaking = false;
        }

        const utterance = new SpeechSynthesisUtterance(text);
        
        // Set state when speech starts and ends
        utterance.onstart = () => {
            isSpeaking = true;
        };
        utterance.onend = () => {
            isSpeaking = false;
        };
        utterance.onerror = (event) => {
            console.error("SpeechSynthesisUtterance.onerror", event);
            alert("An error occurred during speech synthesis.");
            isSpeaking = false;
        };
        
        // Cancel any previously queued speech and speak the new utterance
        speechSynthesis.cancel(); 
        speechSynthesis.speak(utterance);
    }
    
    function copyToClipboard(elementId) {
        const text = document.getElementById(elementId).value;
        if (!text) return;
        navigator.clipboard.writeText(text).then(() => {
            alert("Text copied to clipboard!");
        }).catch((error) => {
            console.error("Error copying text:", error);
            alert("Failed to copy text.");
        });
    }

    function displayAnalysisResults(analysisData, translatedFeedback) {
        elements.resultElement.innerHTML = `<span style="color:#264d54;">Emotion: ${analysisData.feedback_type}, Confidence: ${analysisData.emotion_score.toFixed(2)}</span>`;

        elements.resultContainer.style.display = "block"; // Changed from 'flex' to 'block' to respect container flow
        elements.translatedFeedbackElement.value = translatedFeedback;

        const dominantWordsElement = document.getElementById("dominant-words");
        if (analysisData.dominant_words && Object.keys(analysisData.dominant_words).length > 0) {
            let dominantWordsText = "";
            for (const [emotion, words] of Object.entries(analysisData.dominant_words)) {
                if (words.length > 0) {
                    const emotionColor = `<span style="color:#264d54; font-weight:bold;">${emotion.charAt(0).toUpperCase() + emotion.slice(1)}</span>`;
                    dominantWordsText += `${emotionColor}: ${words.join(", ")}<br>`;
                }
            }
            dominantWordsElement.innerHTML = dominantWordsText;
        } else {
            dominantWordsElement.textContent = "No dominant words detected.";
        }
    }
});