import React, { useState, useEffect, useRef, useMemo } from 'react';
import axios from 'axios';
import ForceGraph3D from 'react-force-graph-3d';
import { Rocket, Send, Database, Share2, Info, Activity, Star, Sparkles, Zap, Cpu, Globe, Shield } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import * as THREE from 'three';
import SpriteText from 'three-spritetext';
import ReactMarkdown from 'react-markdown';

const API_BASE = 'http://localhost:8000';

const App = () => {
  const [messages, setMessages] = useState([
    { role: 'bot', content: '🌌 **AstroGraph Cognitive Core Online**. Agentic RAG active with GraphDB + Owlready2 reasoning.' }
  ]);
  const [input, setInput] = useState('');
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [activeTab, setActiveTab] = useState('chat');
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);
  const fgRef = useRef();


  useEffect(() => {
    fetchGraph();
  }, []);

  useEffect(() => {
    // Balanced Physics Tuning
    if (fgRef.current) {
      fgRef.current.d3Force('charge').strength(-800);
      fgRef.current.d3Force('link').distance(100);
    }
  }, [graphData]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchGraph = async () => {
    try {
      const resp = await axios.get(`${API_BASE}/graph/summary`);
      const { data } = resp.data;
      setGraphData({
        nodes: data.nodes,
        links: data.edges.map(e => ({ source: e.source, target: e.target, label: e.label }))
      });
    } catch (err) {
      console.error('Failed to fetch graph', err);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const resp = await axios.post(`${API_BASE}/chat`, { message: input });
      setMessages(prev => [...prev, { role: 'bot', content: resp.data.reply }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'bot', content: '⚠ **CORE SYSTEM ERROR**: Reasoning engine unreachable. Ensure backend is running on port 8000.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-[#050510] text-gray-100 font-sans overflow-hidden selection:bg-purple-500 selection:text-white relative">

      {/* Sidebar */}
      <motion.div
        initial={{ x: -100, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="w-72 m-4 mr-0 p-6 flex flex-col relative z-20 backdrop-blur-2xl bg-white/5 border border-white/10 rounded-3xl shadow-2xl"
      >
        <div className="flex items-center gap-4 mb-10 pb-6 border-b border-white/10">
          <div className="p-3 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl shadow-[0_0_20px_rgba(139,92,246,0.3)]">
            <Globe size={28} className="text-white animate-spin-slow" />
          </div>
          <div>
            <h1 className="text-2xl font-black bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 tracking-tight">ASTROGRAPH</h1>
            <div className="flex items-center gap-2 mt-1">
              <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
              <p className="text-[10px] text-gray-400 font-mono tracking-widest uppercase">3D SYSTEM ACTIVE</p>
            </div>
          </div>
        </div>

        <nav className="space-y-4 flex-grow">
          {[
            { id: 'chat', label: 'NEURAL LINK', icon: Sparkles, desc: 'Agentic Interface' },
            { id: 'visualizer', label: 'HOLO-MAP', icon: Share2, desc: '3D Visualization' },
            { id: 'data', label: 'DATA VAULT', icon: Database, desc: 'Mission Records' },
          ].map(item => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full text-left group relative overflow-hidden rounded-xl transition-all duration-300 ${activeTab === item.id
                ? 'bg-gradient-to-r from-purple-500/10 to-blue-500/10 border border-purple-500/30'
                : 'hover:bg-white/5 border border-transparent'
                }`}
            >
              <div className="flex items-center gap-4 p-4 z-10 relative">
                <div className={`p-2 rounded-lg transition-colors ${activeTab === item.id ? 'bg-purple-500/20 text-purple-300' : 'bg-white/5 text-gray-400 group-hover:text-white'}`}>
                  <item.icon size={20} />
                </div>
                <div>
                  <span className={`block font-bold text-sm tracking-wide ${activeTab === item.id ? 'text-white' : 'text-gray-400 group-hover:text-white'}`}>
                    {item.label}
                  </span>
                  <span className="text-[10px] text-gray-500 font-mono">{item.desc}</span>
                </div>
              </div>
              {activeTab === item.id && (
                <motion.div
                  layoutId="activeTab"
                  className="absolute inset-0 bg-gradient-to-r from-purple-500/5 to-transparent z-0"
                />
              )}
            </button>
          ))}
        </nav>
      </motion.div>

      {/* Main Content */}
      <div className="flex-grow m-4 flex flex-col relative z-20 overflow-hidden">
        <AnimatePresence mode="wait">
          {activeTab === 'chat' && (
            <motion.div
              key="chat"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.98 }}
              className="flex-grow flex flex-col h-full bg-white/5 backdrop-blur-3xl border border-white/10 rounded-3xl shadow-2xl relative overflow-hidden"
            >
              {/* Messages */}
              <div className="flex-grow p-8 overflow-y-auto space-y-6 scroll-smooth">
                {messages.map((m, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: m.role === 'user' ? 20 : -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3 }}
                    className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`max-w-[70%] p-6 rounded-2xl relative overflow-hidden ${m.role === 'user'
                      ? 'bg-gradient-to-br from-purple-600 to-blue-600 text-white rounded-tr-sm shadow-xl'
                      : 'bg-[#1a1d26] border border-white/10 text-gray-200 rounded-tl-sm shadow-lg'
                      }`}>
                      <div className="relative z-10 text-sm leading-relaxed prose prose-invert max-w-none">
                        <ReactMarkdown>{m.content}</ReactMarkdown>
                      </div>
                    </div>
                  </motion.div>
                ))}
                <div ref={chatEndRef} />
              </div>

              {/* Input Area */}
              <div className="p-6 bg-black/20 border-t border-white/5 backdrop-blur-md">
                <div className="relative flex gap-3">
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    placeholder="Enter mission parameters..."
                    className="flex-grow bg-[#0b0d17] border border-white/10 text-white p-4 rounded-xl focus:outline-none focus:border-purple-500/50"
                  />
                  <button
                    onClick={handleSend}
                    className="bg-gradient-to-r from-purple-500 to-pink-500 text-white p-4 rounded-xl hover:shadow-purple-500/40 transition-all"
                  >
                    <Send size={20} />
                  </button>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'visualizer' && (
            <motion.div
              key="visualizer"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex-grow h-full bg-[#000000] rounded-3xl overflow-hidden relative border border-white/10 shadow-2xl"
            >
              <div className="absolute top-8 left-8 z-20 pointer-events-none">
                <h1 className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-500">GALAXY MAP 3D</h1>
                <p className="text-sm text-purple-400 font-mono mt-2 tracking-widest">INTERACTIVE VIEW</p>
              </div>

              <ForceGraph3D
                ref={fgRef}
                graphData={graphData}
                nodeAutoColorBy="group"
                nodeLabel="id"
                backgroundColor="#000000"

                // Physics Stability
                d3AlphaDecay={0.02}
                d3VelocityDecay={0.3}
                warmupTicks={100}

                // Edges
                linkColor={() => "rgba(255, 255, 255, 0.2)"}
                linkWidth={0.5}
                linkDirectionalParticles={2}
                linkDirectionalParticleSpeed={0.005}
                linkDirectionalParticleWidth={1.5}
                linkDirectionalParticleColor={() => "#a855f7"}

                // Nodes with Geometry + Text
                nodeThreeObject={node => {
                  const group = new THREE.Group();

                  // 1. Sphere Geometry
                  const color = node.id.includes('Mission') ? '#c084fc' : '#38bdf8';
                  const geometry = new THREE.SphereGeometry(3, 16, 16);
                  const material = new THREE.MeshLambertMaterial({
                    color: color,
                    transparent: true,
                    opacity: 0.8,
                    emissive: color,
                    emissiveIntensity: 0.2
                  });
                  const sphere = new THREE.Mesh(geometry, material);
                  group.add(sphere);

                  // 2. Text Label
                  const sprite = new SpriteText(node.id);
                  sprite.color = 'rgba(255, 255, 255, 0.9)';
                  sprite.textHeight = 3;
                  sprite.position.y = 5; // Float above sphere
                  sprite.fontFace = "Inter";
                  group.add(sprite);

                  return group;
                }}
                nodeThreeObjectExtend={false} // We are replacing the object entirely
              />
            </motion.div>
          )}

          {activeTab === 'data' && (
            <motion.div
              key="data"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex-grow h-full bg-white/5 backdrop-blur-3xl border border-white/10 rounded-3xl p-8 overflow-y-auto"
            >
              <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-400 mb-6">MISSION ARCHIVES</h1>

              <div className="bg-black/20 p-6 rounded-2xl border border-white/5 mb-8">
                <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                  <Database size={20} className="text-purple-400" /> Dynamic KRR Ingestion
                </h2>
                <div className="flex gap-4 items-center">
                  <input
                    type="file"
                    id="file-upload"
                    className="hidden"
                    onChange={async (e) => {
                      const file = e.target.files[0];
                      if (!file) return;

                      const formData = new FormData();
                      formData.append('file', file);

                      try {
                        alert("Initiating secure upload & ontology mapping...");
                        const res = await axios.post(`${API_BASE}/upload`, formData);
                        alert(`Success! Knowledge Graph updated with ${res.data.triples_added} new facts.`);
                        window.location.reload(); // Refresh graph
                      } catch (err) {
                        alert("Ingestion Failed: " + err.message);
                      }
                    }}
                  />
                  <label htmlFor="file-upload" className="cursor-pointer bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl font-bold transition-all shadow-lg hover:shadow-purple-500/30 flex items-center gap-2">
                    <Rocket size={18} /> UPLOAD MISSION DOC
                  </label>
                  <p className="text-gray-400 text-sm">Supports: .txt, .csv (Auto-mapped to Ontology)</p>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default App;
