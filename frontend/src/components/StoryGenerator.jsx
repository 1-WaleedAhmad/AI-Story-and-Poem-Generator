import React, { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, BookOpen, Feather, Settings, Send, Loader2, Copy, Check, Github } from 'lucide-react';
import './StoryGenerator.css';

const StoryGenerator = () => {
    const [prompt, setPrompt] = useState('');
    const [type, setType] = useState('story');
    const [temperature, setTemperature] = useState(0.8);
    const [topK, setTopK] = useState(50);
    const [topP, setTopP] = useState(0.95);
    const [isGenerating, setIsGenerating] = useState(false);
    const [result, setResult] = useState('');
    const [showSettings, setShowSettings] = useState(false);
    const [copied, setCopied] = useState(false);

    const handleGenerate = async () => {
        if (!prompt.trim()) return;

        setIsGenerating(true);
        setResult('');

        const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

        try {
            const response = await axios.post(`${API_URL}/generate`, {
                prompt: prompt,
                type: type,
                temperature: temperature,
                top_k: topK,
                top_p: topP,
                max_new_tokens: 150
            });

            if (response.data && response.data.result) {
                setResult(response.data.result);
            } else {
                throw new Error('Invalid response format');
            }
        } catch (error) {
            console.error('Generation failed:', error);
            setResult(`Error: Failed to generate content.\n\nDetails: ${error.message}`);
        } finally {
            setIsGenerating(false);
        }
    };

    const copyToClipboard = () => {
        navigator.clipboard.writeText(result);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    const openGithubProfiles = () => {
        window.open('https://github.com/aay-zee', '_blank');
        setTimeout(() => {
            window.open('https://github.com/1-WaleedAhmad', '_blank');
        }, 100);
    };

    return (
        <div className="generator-container">
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="header"
            >
                <div className="logo-container">
                    <Sparkles className="logo-icon" size={32} />
                    <h1>AI Story & Poem Generator</h1>
                </div>
                <p className="subtitle">Unleash your imagination with the power of AI</p>
            </motion.div>

            <div className="main-content">
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                    className="input-section"
                >
                    <div className="input-card">
                        <div className="tabs">
                            <button
                                className={`tab ${type === 'story' ? 'active' : ''}`}
                                onClick={() => setType('story')}
                            >
                                <BookOpen size={18} />
                                <span>Story</span>
                            </button>
                            <button
                                className={`tab ${type === 'poem' ? 'active' : ''}`}
                                onClick={() => setType('poem')}
                            >
                                <Feather size={18} />
                                <span>Poem</span>
                            </button>
                        </div>

                        <textarea
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            placeholder={`Enter a theme or prompt for your ${type}... (e.g., "A rainy day in Tokyo")`}
                            className="prompt-input"
                            rows={5}
                        />

                        <div className="controls-bar">
                            <button
                                className={`settings-toggle ${showSettings ? 'active' : ''}`}
                                onClick={() => setShowSettings(!showSettings)}
                            >
                                <Settings size={18} />
                                <span>Parameters</span>
                            </button>

                            <button
                                className="generate-btn"
                                onClick={handleGenerate}
                                disabled={isGenerating || !prompt.trim()}
                            >
                                {isGenerating ? (
                                    <>
                                        <Loader2 size={18} className="spin" />
                                        <span>Generating...</span>
                                    </>
                                ) : (
                                    <>
                                        <Send size={18} />
                                        <span>Generate</span>
                                    </>
                                )}
                            </button>
                        </div>

                        <AnimatePresence>
                            {showSettings && (
                                <motion.div
                                    initial={{ height: 0, opacity: 0 }}
                                    animate={{ height: 'auto', opacity: 1 }}
                                    exit={{ height: 0, opacity: 0 }}
                                    className="settings-panel"
                                >
                                    <div className="setting-item">
                                        <label>Temperature: {temperature}</label>
                                        <input
                                            type="range"
                                            min="0.1"
                                            max="1.5"
                                            step="0.1"
                                            value={temperature}
                                            onChange={(e) => setTemperature(parseFloat(e.target.value))}
                                        />
                                        <span className="tooltip">Creativity vs Coherence</span>
                                    </div>
                                    <div className="setting-item">
                                        <label>Top-K: {topK}</label>
                                        <input
                                            type="range"
                                            min="1"
                                            max="100"
                                            step="1"
                                            value={topK}
                                            onChange={(e) => setTopK(parseInt(e.target.value))}
                                        />
                                    </div>
                                    <div className="setting-item">
                                        <label>Top-P: {topP}</label>
                                        <input
                                            type="range"
                                            min="0.1"
                                            max="1.0"
                                            step="0.05"
                                            value={topP}
                                            onChange={(e) => setTopP(parseFloat(e.target.value))}
                                        />
                                    </div>
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5, delay: 0.4 }}
                    className="output-section"
                >
                    <div className="output-card">
                        <div className="output-header">
                            <h3>Generated Result</h3>
                            {result && (
                                <button className="copy-btn" onClick={copyToClipboard}>
                                    {copied ? <Check size={16} /> : <Copy size={16} />}
                                </button>
                            )}
                        </div>

                        <div className="output-content">
                            {isGenerating ? (
                                <div className="placeholder-loading">
                                    <div className="shimmer-line"></div>
                                    <div className="shimmer-line short"></div>
                                    <div className="shimmer-line"></div>
                                </div>
                            ) : result ? (
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="result-text"
                                >
                                    {result.split('\n').map((line, i) => (
                                        <p key={i}>{line}</p>
                                    ))}
                                </motion.div>
                            ) : (
                                <div className="empty-state">
                                    <Sparkles size={48} className="empty-icon" />
                                    <p>Your creative masterpiece will appear here.</p>
                                </div>
                            )}
                        </div>
                    </div>
                </motion.div>
            </div>

            <motion.button
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="github-float-btn"
                onClick={openGithubProfiles}
                title="View Contributors"
            >
                <Github size={24} />
            </motion.button>
        </div>
    );
};

export default StoryGenerator;
