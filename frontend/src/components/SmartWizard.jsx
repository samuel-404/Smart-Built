import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import gsap from 'gsap';
import * as THREE from 'three';

// ─── Animation presets ───────────────────────────────────────
const ease = { duration: 0.4, ease: [0.25, 0.1, 0.25, 1] };

const Icons = {
  gamepad: () => (<svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" /></svg>),
  video: () => (<svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>),
  book: () => (<svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>),
  briefcase: () => (<svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>),
  cpu: () => (<svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" /></svg>),
  gpu: () => (<svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 7h16M4 7v10a2 2 0 002 2h12a2 2 0 002-2V7M4 7l2-3h12l2 3M8 11h.01M12 11h.01M16 11h.01" /></svg>),
  mobo: () => (<svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M6 19h12a2 2 0 002-2V7a2 2 0 00-2-2H6a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>),
  ram: () => (<svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 6h16v12H4V6zm2 3v6m3-6v6m3-6v6m3-6v6" /></svg>),
  storage: () => (<svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" /></svg>),
  psu: () => (<svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>),
  pcCase: () => (<svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M5 3h14a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2zm3 4h8M8 9h3" /></svg>),
  check: () => (<svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>),
  arrowRight: () => (<svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" /></svg>),
  arrowLeft: () => (<svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>),
  sparkle: () => (<svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" /></svg>),
  swap: () => (<svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" /></svg>),
  close: () => (<svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>),
  refresh: () => (<svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>),
  intel: () => (<svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M20.42 7.345v9.18h1.651v-9.18zM0 7.475v1.737h1.737V7.474zm9.78.352v6.053c0 .513.044.945.13 1.292.087.34.235.618.44.828.203.21.475.359.803.451.334.093.754.136 1.255.136h.216v-1.533c-.24 0-.445-.012-.593-.037a.672.672 0 0 1-.39-.173.693.693 0 0 1-.173-.377 4.002 4.002 0 0 1-.037-.606v-2.182h1.193v-1.416h-1.193V7.827zm-3.505 2.312c-.396 0-.76.08-1.082.241-.327.161-.6.384-.822.668l-.087.117v-.902H2.658v6.256h1.639v-3.214c.018-.588.16-1.02.433-1.299.29-.297.642-.445 1.044-.445.476 0 .841.149 1.082.433.235.284.359.686.359 1.2v3.324h1.663V12.97c.006-.89-.229-1.595-.686-2.09-.458-.495-1.1-.742-1.917-.742zm10.065.006a3.252 3.252 0 0 0-2.306.946c-.29.29-.525.637-.692 1.033a3.145 3.145 0 0 0-.254 1.273c0 .452.08.878.241 1.274.161.395.39.742.674 1.032.284.29.637.526 1.045.693.408.173.86.26 1.342.26 1.397 0 2.262-.637 2.782-1.23l-1.187-.904c-.248.297-.841.699-1.583.699-.464 0-.847-.105-1.138-.321a1.588 1.588 0 0 1-.593-.872l-.019-.056h4.915v-.587c0-.451-.08-.872-.235-1.267a3.393 3.393 0 0 0-.661-1.033 3.013 3.013 0 0 0-1.02-.692 3.345 3.345 0 0 0-1.311-.248zm-16.297.118v6.256h1.651v-6.256zm16.278 1.286c1.132 0 1.664.797 1.664 1.255l-3.32.006c0-.458.525-1.255 1.656-1.261zm7.073 3.814a.606.606 0 0 0-.606.606.606.606 0 0 0 .606.606.606.606 0 0 0 .606-.606.606.606 0 0 0-.606-.606zm-.008.105a.5.5 0 0 1 .002 0 .5.5 0 0 1 .5.501.5.5 0 0 1-.5.5.5.5 0 0 1-.5-.5.5.5 0 0 1 .498-.5zm-.233.155v.699h.13v-.285h.093l.173.285h.136l-.18-.297a.191.191 0 0 0 .118-.056c.03-.03.05-.074.05-.136 0-.068-.02-.117-.063-.154-.037-.038-.105-.056-.185-.056zm.13.099h.154c.019 0 .037.006.056.012a.064.064 0 0 1 .037.031c.013.013.012.031.012.056a.124.124 0 0 1-.012.055.164.164 0 0 1-.037.031c-.019.006-.037.013-.056.013h-.154Z" /></svg>),
  amd: () => (<svg className="w-8 h-8" fill="currentColor" viewBox="0 0 24 24"><path d="M18.324 9.137l1.559 1.56h2.556v2.557L24 14.814V9.137zM2 9.52l-2 4.96h1.309l.37-.982H3.9l.408.982h1.338L3.432 9.52zm4.209 0v4.955h1.238v-3.092l1.338 1.562h.188l1.338-1.556v3.091h1.238V9.52H10.47l-1.592 1.845L7.287 9.52zm6.283 0v4.96h2.057c1.979 0 2.88-1.046 2.88-2.472 0-1.36-.937-2.488-2.747-2.488zm1.237.91h.792c1.17 0 1.63.711 1.63 1.57 0 .728-.372 1.572-1.616 1.572h-.806zm-10.985.273l.791 1.932H2.008zm17.137.307l-1.604 1.603v2.25h2.246l1.604-1.607h-2.246z" /></svg>),
};

const compIcons = { cpu: Icons.cpu, gpu: Icons.gpu, motherboard: Icons.mobo, ram: Icons.ram, storage: Icons.storage, psu: Icons.psu, case: Icons.pcCase };
const compLabels = { cpu: 'Processor', gpu: 'Graphics Card', motherboard: 'Motherboard', ram: 'Memory', storage: 'Storage', psu: 'Power Supply', case: 'Case' };
const formatPrice = (p) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(p);

// ─── Gaming PC Hero Image ────────────────────────────────────
const GamingPCHero = () => (
  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', width: '100%', height: '100%' }}>
    <img
      src="/detailed_gaming_pc_transparent.png"
      alt="Gaming PC Build"
      style={{
        maxHeight: '100%',
        maxWidth: '90%',
        objectFit: 'contain',
        filter: 'drop-shadow(0 20px 40px rgba(0,0,0,0.08))',
      }}
    />
  </div>
);



// ─── Glass Nav ───────────────────────────────────────────────
const Header = ({ showBack, onBack }) => (
  <header className="glass-nav sticky top-0 z-50" style={{ borderBottom: '1px solid rgba(0,0,0,0.06)' }}>
    <div className="max-w-5xl mx-auto px-6 py-3.5 flex items-center justify-between">
      <div className="flex items-center gap-3">
        {showBack && (
          <button onClick={onBack} className="p-1.5 rounded-lg mr-1 hover:bg-black/[0.04]" style={{ color: '#86868B' }}>
            <Icons.arrowLeft />
          </button>
        )}
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg flex items-center justify-center" style={{ background: '#1D1D1F', color: '#fff' }}>
            <Icons.cpu />
          </div>
          <span className="text-base font-semibold tracking-tight" style={{ color: '#1D1D1F' }}>SmartBuild</span>
        </div>
      </div>
      <div className="hidden sm:flex items-center gap-1.5 text-xs font-medium" style={{ color: '#86868B' }}>
        <Icons.sparkle /><span>AI-Powered</span>
      </div>
    </div>
  </header>
);

// ─── Landing Page with Three.js Hero ─────────────────────────
const LandingPage = ({ onGetStarted }) => {
  const useCases = [
    { icon: Icons.gamepad, label: 'Gaming' },
    { icon: Icons.video, label: 'Content' },
    { icon: Icons.book, label: 'Student' },
    { icon: Icons.briefcase, label: 'Work' },
  ];
  return (
    <div className="min-h-screen" style={{ background: '#F5F5F7' }}>
      <Header showBack={false} />
      <main className="max-w-3xl mx-auto px-6 pt-16 pb-24 relative">
        {/* Three.js Gaming PC hero */}
        <div className="relative h-96 mb-2">
          <GamingPCHero />
        </div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, ease: [0.25, 0.1, 0.25, 1] }} className="text-center mb-16">
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight mb-4" style={{ color: '#1D1D1F', lineHeight: 1.08 }}>
            Build Your<br />Perfect PC.
          </h1>
          <p className="text-lg mb-10 max-w-md mx-auto" style={{ color: '#86868B', lineHeight: 1.5 }}>
            Set a budget. Pick a use case.<br />Let the AI optimizer do the rest.
          </p>
          <div className="flex justify-center gap-2 mb-10">
            {useCases.map(uc => (
              <div key={uc.label} className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium" style={{ color: '#86868B', background: 'rgba(0,0,0,0.03)' }}>
                <uc.icon /><span>{uc.label}</span>
              </div>
            ))}
          </div>
          <motion.button onClick={onGetStarted} whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-full text-base font-semibold shadow-lg"
            style={{ background: '#0071E3', color: '#fff', boxShadow: '0 4px 14px rgba(0,113,227,0.25)' }}>
            Get Started <Icons.arrowRight />
          </motion.button>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.2 }} className="soft-card p-10">
          <h2 className="text-lg font-semibold tracking-tight mb-8 text-center" style={{ color: '#1D1D1F' }}>How It Works</h2>
          <div className="grid md:grid-cols-3 gap-10">
            {[{ s: '01', t: 'Set Budget', d: 'Define your spending limit' }, { s: '02', t: 'Choose Use Case', d: 'Pick your primary workload' }, { s: '03', t: 'Get Builds', d: 'AI-optimized part lists' }].map(item => (
              <div key={item.s} className="text-center">
                <div className="w-10 h-10 rounded-2xl flex items-center justify-center text-sm font-bold mx-auto mb-3" style={{ background: '#F5F5F7', color: '#1D1D1F' }}>{item.s}</div>
                <h3 className="font-semibold text-sm mb-1" style={{ color: '#1D1D1F' }}>{item.t}</h3>
                <p className="text-xs" style={{ color: '#86868B' }}>{item.d}</p>
              </div>
            ))}
          </div>
        </motion.div>
      </main>
    </div>
  );
};

// ─── Step Indicator ──────────────────────────────────────────
const StepIndicator = ({ currentStep, steps }) => (
  <div className="flex items-center justify-center mb-10">
    {steps.map((label, i) => (
      <React.Fragment key={i}>
        <div className="flex flex-col items-center">
          <div className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold"
            style={currentStep > i ? { background: '#1D1D1F', color: '#fff' } : currentStep === i ? { background: '#0071E3', color: '#fff' } : { background: '#E8E8ED', color: '#86868B' }}>
            {currentStep > i ? <Icons.check /> : i + 1}
          </div>
          <span className="text-[11px] mt-2 font-medium" style={{ color: currentStep >= i ? '#1D1D1F' : '#86868B' }}>{label}</span>
        </div>
        {i < steps.length - 1 && <div className="w-14 h-[2px] mx-2 mt-[-12px] rounded-full" style={{ background: currentStep > i ? '#1D1D1F' : '#E8E8ED' }} />}
      </React.Fragment>
    ))}
  </div>
);

// ─── Budget Step ─────────────────────────────────────────────
const BudgetStep = ({ budget, setBudget, onNext }) => {
  const tiers = [{ min: 35000, max: 50000, label: 'Budget' }, { min: 50000, max: 80000, label: 'Mid-Range' }, { min: 80000, max: 120000, label: 'High-End' }, { min: 120000, max: 200000, label: 'Enthusiast' }, { min: 200000, max: 500000, label: 'Premium' }];
  const tier = tiers.find(t => budget >= t.min && budget <= t.max) || tiers[0];
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} transition={ease} className="space-y-8">
      <div className="text-center">
        <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ color: '#1D1D1F' }}>What's your budget?</h2>
        <p className="text-sm" style={{ color: '#86868B' }}>Slide to set your maximum spend</p>
      </div>
      <div className="text-center py-6">
        <div className="text-5xl font-bold tracking-tight mb-3" style={{ color: '#1D1D1F' }}>{formatPrice(budget)}</div>
        <span className="inline-block px-3 py-1 rounded-full text-xs font-medium" style={{ color: '#0071E3', background: 'rgba(0,113,227,0.08)' }}>{tier.label} Tier</span>
      </div>
      <div className="px-2">
        <input type="range" min="35000" max="500000" step="5000" value={budget} onChange={e => setBudget(parseInt(e.target.value))} className="w-full cursor-pointer"
          style={{ background: `linear-gradient(to right, #0071E3 0%, #0071E3 ${((budget - 35000) / 465000) * 100}%, #E8E8ED ${((budget - 35000) / 465000) * 100}%, #E8E8ED 100%)` }} />
        <div className="flex justify-between text-xs mt-2" style={{ color: '#86868B' }}><span>₹35,000</span><span>₹5,00,000</span></div>
      </div>
      <div className="grid grid-cols-5 gap-2">
        {tiers.map(t => (
          <button key={t.label} onClick={() => setBudget(Math.floor((t.min + t.max) / 2))}
            className="p-2.5 rounded-xl text-center text-xs font-medium transition-all"
            style={tier.label === t.label ? { background: 'rgba(0,113,227,0.08)', color: '#0071E3', boxShadow: '0 0 0 1.5px #0071E3' } : { background: '#fff', color: '#86868B', boxShadow: 'var(--shadow-xs)' }}>
            {t.label}
          </button>
        ))}
      </div>
      <div className="flex justify-end pt-2">
        <motion.button onClick={onNext} whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.98 }}
          className="flex items-center gap-2 px-7 py-3 rounded-full text-sm font-semibold" style={{ background: '#0071E3', color: '#fff' }}>
          Continue <Icons.arrowRight />
        </motion.button>
      </div>
    </motion.div>
  );
};

// ─── Usage Step ──────────────────────────────────────────────
const UsageStep = ({ usageType, setUsageType, onNext, onBack }) => {
  const usageGroups = [
    {
      category: 'Gaming & Streaming PC',
      icon: Icons.gamepad,
      color: '#A855F7',
      bgOpacity: 'rgba(168, 85, 247, 0.1)',
      items: [
        { id: 'gaming_esports', name: 'Esports Gaming PC' },
        { id: 'gaming_casual', name: 'Casual Gaming PC' },
        { id: 'gaming_aaa', name: 'AAA Gaming PC' }
      ]
    },
    {
      category: 'Streaming & Simulator PC',
      icon: Icons.video,
      color: '#EC4899',
      bgOpacity: 'rgba(236, 72, 153, 0.1)',
      items: [
        { id: 'streaming_mobile', name: 'Mobile Streaming PC' },
        { id: 'streaming_pc', name: 'PC Streaming PC' },
        { id: 'streaming_vr', name: 'VR Gaming PC' },
        { id: 'simulator', name: 'Simulator PC' }
      ]
    },
    {
      category: 'Music Production PCs',
      icon: Icons.sparkle,
      color: '#EAB308',
      bgOpacity: 'rgba(234, 179, 8, 0.1)',
      items: [
        { id: 'music_flstudio', name: 'FL Studio PC' },
        { id: 'music_ableton', name: 'Ableton PC' }
      ]
    },
    {
      category: 'Video Editing PC',
      icon: Icons.video,
      color: '#F97316',
      bgOpacity: 'rgba(249, 115, 22, 0.1)',
      items: [
        { id: 'video_premiere', name: 'Adobe Premiere Pro' },
        { id: 'video_davinci', name: 'Davinci Resolve Studio' }
      ]
    },
    {
      category: 'Layout & 3D Generalist',
      icon: Icons.briefcase,
      color: '#06B6D4',
      bgOpacity: 'rgba(6, 182, 212, 0.1)',
      items: [
        { id: 'layout3d_maya', name: 'Maya PC' },
        { id: 'layout3d_cinema4d', name: 'Cinema 4D PC' }
      ]
    },
    {
      category: 'Game Development PC',
      icon: Icons.cpu,
      color: '#14B8A6',
      bgOpacity: 'rgba(20, 184, 166, 0.1)',
      items: [
        { id: 'gamedev_unity', name: 'Unity PC' },
        { id: 'gamedev_ue5', name: 'Unreal Engine 5 PC' },
        { id: 'gamedev_blender', name: 'Blender PC' }
      ]
    },
    {
      category: 'Architectural PC',
      icon: Icons.book,
      color: '#8B5CF6',
      bgOpacity: 'rgba(139, 92, 246, 0.1)',
      items: [
        { id: 'arch_autocad', name: 'AutoCAD PC' },
        { id: 'arch_sketchup', name: 'Sketchup PC' },
        { id: 'arch_revit', name: 'Revit PC' },
        { id: 'arch_vray', name: 'V-Ray PC' },
        { id: 'arch_corona', name: 'Corona Render PC' },
        { id: 'arch_octane', name: 'Octane Render PC' }
      ]
    },
    {
      category: '3D Modelling PC',
      icon: Icons.gpu,
      color: '#3B82F6',
      bgOpacity: 'rgba(59, 130, 246, 0.1)',
      items: [
        { id: 'model3d_blender', name: 'Blender PC' },
        { id: 'model3d_lumion', name: 'Lumion PC' },
        { id: 'model3d_3dsmax', name: '3DsMax PC' },
        { id: 'model3d_solidworks', name: 'Solidworks PC' }
      ]
    },
    {
      category: 'VFX & Compositing PC',
      icon: Icons.video,
      color: '#6366F1',
      bgOpacity: 'rgba(99, 102, 241, 0.1)',
      items: [
        { id: 'vfx_nuke', name: 'Nuke PC' },
        { id: 'vfx_houdini', name: 'Houdini PC' },
        { id: 'comp_aftereffects', name: 'After Effects PC' }
      ]
    },
    {
      category: 'Graphic Designing PCs',
      icon: Icons.sparkle,
      color: '#10B981',
      bgOpacity: 'rgba(16, 185, 129, 0.1)',
      items: [
        { id: 'graphic_photoshop', name: 'Photoshop PC' },
        { id: 'graphic_illustrator', name: 'Illustrator PC' },
        { id: 'graphic_corel', name: 'Corel Draw Suite' },
        { id: 'graphic_figma', name: 'Figma PC' }
      ]
    },
    {
      category: 'Corporate Use Case',
      icon: Icons.briefcase,
      color: '#64748B',
      bgOpacity: 'rgba(100, 116, 139, 0.1)',
      items: [
        { id: 'corp_ai', name: 'AI & DeepLearning PC' },
        { id: 'corp_coding', name: 'Coding PC' },
        { id: 'corp_trading', name: 'Trading PC' },
        { id: 'corp_office', name: 'Home & Office PC' },
        { id: 'corp_signage', name: 'Digital Signage PC' }
      ]
    }
  ];

  const [activeGroup, setActiveGroup] = useState(null);

  // Find selected item name for button summary
  let selectedItemName = "None";
  usageGroups.forEach(g => {
    const found = g.items.find(i => i.id === usageType);
    if (found) selectedItemName = found.name;
  });

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} transition={ease} className="space-y-6 font-sans">
      <div className="text-center mb-4">
        <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ color: '#1D1D1F' }}>What will you use it for?</h2>
        <p className="text-sm" style={{ color: '#86868B' }}>Select your exact use-case profile</p>
      </div>

      <div className="max-h-[50vh] overflow-y-auto pr-2 pb-4 scrollbar-hide space-y-3">
        {usageGroups.map((g, i) => {
          const isActive = activeGroup === i;
          const hasSelected = g.items.some(item => item.id === usageType);

          return (
            <div key={i} className="soft-card overflow-hidden transition-all duration-300"
              style={{ border: hasSelected ? `1.5px solid ${g.color}` : '1.5px solid transparent' }}>
              <button
                onClick={() => setActiveGroup(isActive ? null : i)}
                className="w-full flex items-center justify-between p-4 text-left hover:bg-black/[0.02] transition-colors"
                style={{ background: hasSelected ? g.bgOpacity : '#fff' }}
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl flex items-center justify-center transition-colors"
                    style={{ background: isActive || hasSelected ? g.color : '#F5F5F7', color: isActive || hasSelected ? '#fff' : '#86868B' }}>
                    <g.icon />
                  </div>
                  <div>
                    <h3 className="font-semibold text-sm" style={{ color: '#1D1D1F' }}>{g.category}</h3>
                    <p className="text-xs" style={{ color: '#86868B' }}>{g.items.length} specific profiles</p>
                  </div>
                </div>
                <div className="transform transition-transform duration-300" style={{ transform: isActive ? 'rotate(90deg)' : 'rotate(0deg)', color: '#86868B' }}>
                  <Icons.arrowRight />
                </div>
              </button>

              <AnimatePresence>
                {isActive && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={ease}
                    className="bg-white border-t border-gray-100"
                  >
                    <div className="p-4 grid grid-cols-2 gap-2">
                      {g.items.map(item => {
                        const isSelected = usageType === item.id;
                        return (
                          <button
                            key={item.id}
                            onClick={() => { setUsageType(item.id); setActiveGroup(null); }}
                            className="p-3 rounded-xl text-xs font-medium text-left transition-all border"
                            style={{
                              borderColor: isSelected ? g.color : '#E8E8ED',
                              backgroundColor: isSelected ? g.color : '#fff',
                              color: isSelected ? '#fff' : '#1D1D1F',
                            }}
                          >
                            {item.name}
                          </button>
                        );
                      })}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          );
        })}
      </div>

      <div className="flex justify-between items-center pt-2 border-t border-gray-100 mt-2">
        <button onClick={onBack} className="flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-colors hover:bg-gray-100" style={{ color: '#86868B' }}>
          <Icons.arrowLeft /> Back
        </button>
        <div className="flex items-center gap-4">
          <span className="text-xs font-semibold" style={{ color: '#86868B' }}>
            Selected: <span style={{ color: '#0071E3' }}>{selectedItemName}</span>
          </span>
          <motion.button onClick={onNext} disabled={!usageType} whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
            className="flex items-center gap-2 px-6 py-2.5 rounded-full text-sm font-semibold disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            style={{ background: '#1D1D1F', color: '#fff' }}>
            Continue <Icons.arrowRight />
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
};

// ─── CPU Brand Step ──────────────────────────────────────────
const CpuBrandStep = ({ cpuBrand, setCpuBrand, onNext, onBack }) => {
  const brands = [
    { id: 'Intel', name: 'Intel', desc: 'Core i3, i5, i7, i9', icon: Icons.intel, brandColor: '#0071C5', hoverBg: 'rgba(0,113,197,0.08)' },
    { id: 'AMD', name: 'AMD', desc: 'Ryzen 5, 7, 9', icon: Icons.amd, brandColor: '#ED1C24', hoverBg: 'rgba(237,28,36,0.08)' },
    { id: '', name: 'No Preference', desc: 'Let AI decide', icon: Icons.sparkle, brandColor: '#0071E3', hoverBg: 'rgba(0,113,227,0.08)' },
  ];
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} transition={ease} className="space-y-8 font-sans">
      <div className="text-center">
        <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ color: '#1D1D1F' }}>CPU Brand Preference</h2>
        <p className="text-sm" style={{ color: '#86868B' }}>Choose your preferred processor brand</p>
      </div>
      <div className="grid grid-cols-3 gap-3">
        {brands.map((b, i) => (
          <motion.button key={b.id} onClick={() => setCpuBrand(b.id)} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ ...ease, delay: i * 0.05 }}
            className="p-6 rounded-2xl text-center transition-all group relative overflow-hidden"
            style={cpuBrand === b.id ? { background: '#fff', boxShadow: `0 0 0 2px ${b.brandColor}, 0 4px 12px ${b.hoverBg}` } : { background: '#fff', boxShadow: 'var(--shadow-sm)' }}
            onMouseEnter={(e) => {
              if (cpuBrand !== b.id) {
                e.currentTarget.style.boxShadow = `0 4px 12px ${b.hoverBg}`;
                e.currentTarget.style.borderColor = b.brandColor;
              }
            }}
            onMouseLeave={(e) => {
              if (cpuBrand !== b.id) {
                e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
                e.currentTarget.style.borderColor = 'transparent';
              }
            }}>
            <div className="w-14 h-14 rounded-full inline-flex items-center justify-center mb-4 mx-auto transition-transform duration-300 group-hover:scale-110"
              style={{ background: cpuBrand === b.id ? b.hoverBg : '#F5F5F7', color: cpuBrand === b.id ? b.brandColor : '#86868B' }}>
              <b.icon />
            </div>
            <h3 className="font-semibold text-sm mb-1" style={{ color: '#1D1D1F' }}>{b.name}</h3>
            <p className="text-xs" style={{ color: '#86868B' }}>{b.desc}</p>
          </motion.button>
        ))}
      </div>
      <div className="flex justify-between pt-4 pb-2">
        <button onClick={onBack} className="flex items-center gap-2 px-6 py-2.5 rounded-full text-sm font-medium transition-colors hover:bg-gray-100" style={{ color: '#86868B' }}><Icons.arrowLeft /> Back</button>
        <motion.button onClick={onNext} whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
          className="flex items-center gap-2 px-8 py-3 rounded-full text-sm font-semibold transition-all" style={{ background: '#1D1D1F', color: '#fff' }}>Generate Builds <Icons.arrowRight /></motion.button>
      </div>
    </motion.div>
  );
};

// ─── Loading ─────────────────────────────────────────────────
const LoadingStep = () => {
  const [progress, setProgress] = useState(0);
  useEffect(() => { const t = setInterval(() => setProgress(p => Math.min(p + 2, 95)), 100); return () => clearInterval(t); }, []);
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center py-20">
      <div className="relative w-14 h-14 mx-auto mb-6">
        <div className="absolute inset-0 rounded-full" style={{ border: '2px solid #E8E8ED' }} />
        <div className="absolute inset-0 rounded-full animate-spin" style={{ border: '2px solid transparent', borderTopColor: '#0071E3' }} />
        <div className="absolute inset-0 flex items-center justify-center" style={{ color: '#0071E3' }}><Icons.sparkle /></div>
      </div>
      <h3 className="text-lg font-semibold mb-2" style={{ color: '#1D1D1F' }}>Optimizing</h3>
      <p className="text-xs mb-6" style={{ color: '#86868B' }}>Analyzing component compatibility...</p>
      <div className="w-40 h-1 mx-auto rounded-full overflow-hidden" style={{ background: '#E8E8ED' }}>
        <div className="h-full rounded-full transition-all duration-100" style={{ width: `${progress}%`, background: '#0071E3' }} />
      </div>
    </motion.div>
  );
};

// ─── Build Card (Airy List Rows with GSAP) ───────────────────
const BuildCard = ({ build, index, onSwapComponent, onUpdatePrice }) => {
  const [swapType, setSwapType] = useState(null);
  const [alternatives, setAlternatives] = useState([]);
  const [swapLoading, setSwapLoading] = useState(false);
  const [priceLoading, setPriceLoading] = useState(null);
  const rowsRef = useRef(null);
  const compOrder = ['cpu', 'gpu', 'motherboard', 'ram', 'storage', 'psu', 'case'];
  const API_URL = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '' : 'http://localhost:5000');

  // GSAP staggered reveal on mount
  useEffect(() => {
    if (!rowsRef.current) return;
    const rows = rowsRef.current.querySelectorAll('.comp-row');
    gsap.fromTo(rows,
      { opacity: 0, y: 8, scale: 0.98 },
      { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: 'power2.out', stagger: 0.06, delay: index * 0.15 }
    );
  }, [build, index]);

  const fetchAlts = async (ct) => {
    if (swapType === ct) { setSwapType(null); return; }
    setSwapType(ct); setSwapLoading(true);
    try {
      const r = await fetch(`${API_URL}/api/alternatives`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ component_type: ct, current_build: build.components }) });
      const d = await r.json();
      if (d.success) setAlternatives(d.alternatives);
    } catch (e) { console.error(e); } finally { setSwapLoading(false); }
  };

  const checkLivePrice = async (ct, compId) => {
    if (!compId) return;
    setPriceLoading(ct);
    try {
      const r = await fetch(`${API_URL}/api/prices/update-live`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ component_id: compId }) });
      const d = await r.json();
      if (d.success && d.new_price) {
        if (onUpdatePrice) onUpdatePrice(index, ct, d.new_price);
      }
    } catch (e) { console.error(e); } finally { setPriceLoading(null); }
  };

  const selectAlt = (ct, comp) => { onSwapComponent(index, ct, comp); setSwapType(null); setAlternatives([]); };
  const cpuTdp = build.components.cpu?.tdp || 0;
  const gpuTdp = build.components.gpu?.tdp || 0;
  const estWattage = Math.ceil((cpuTdp + gpuTdp) * 1.3 + 80);

  return (
    <div className="soft-card overflow-hidden">
      {/* Pinned Summary — glass effect */}
      <div className="glass-nav px-6 py-4 flex flex-wrap items-center justify-between gap-3" style={{ borderBottom: '1px solid rgba(0,0,0,0.05)' }}>
        <div className="flex items-center gap-3">
          {index === 0 && <span className="text-[10px] font-bold tracking-widest uppercase px-2.5 py-1 rounded-full" style={{ background: 'rgba(0,113,227,0.08)', color: '#0071E3' }}>RECOMMENDED</span>}
          <span className="text-sm font-semibold" style={{ color: '#1D1D1F' }}>{build.label}</span>
        </div>
        <div className="flex items-center gap-5 text-xs">
          <div><span style={{ color: '#86868B' }}>Total </span><span className="font-bold" style={{ color: '#1D1D1F' }}>{formatPrice(build.total_cost)}</span></div>
          <div><span style={{ color: '#86868B' }}>~</span><span className="font-semibold" style={{ color: '#86868B' }}>{estWattage}W</span></div>
          <div className="flex items-center gap-1"><div className="dot-ok" /><span className="font-medium" style={{ color: '#34C759' }}>Compatible</span></div>
        </div>
      </div>

      {/* Component Rows */}
      <div ref={rowsRef}>
        {compOrder.map((ct) => {
          const comp = build.components[ct];
          const Ic = compIcons[ct];
          const isSwapping = swapType === ct;

          if (ct === 'gpu' && !comp && build.is_apu_build) {
            return (
              <div key={ct} className="comp-row flex items-center px-6 py-5 row-accent" style={{ borderBottom: '1px solid rgba(0,0,0,0.04)' }}>
                <div className="w-9 h-9 rounded-xl flex items-center justify-center mr-5 flex-shrink-0" style={{ background: '#F5F5F7', color: '#34C759' }}><Icons.gpu /></div>
                <div className="flex-1">
                  <div className="text-[10px] font-semibold uppercase tracking-wider mb-0.5" style={{ color: '#86868B' }}>Graphics</div>
                  <div className="text-sm font-medium" style={{ color: '#1D1D1F' }}>{build.igpu_name || 'Integrated Graphics'}</div>
                </div>
                <span className="text-xs font-semibold mr-5" style={{ color: '#34C759' }}>Included with CPU</span>
                <div className="flex items-center gap-1"><div className="dot-ok" /></div>
              </div>
            );
          }
          if (!comp) return null;

          return (
            <React.Fragment key={ct}>
              <div className={`comp-row flex items-center px-6 py-5 row-accent cursor-default transition-shadow ${isSwapping ? '' : ''}`}
                style={{ borderBottom: '1px solid rgba(0,0,0,0.04)', background: isSwapping ? 'rgba(0,113,227,0.02)' : 'transparent' }}>
                <div className="w-9 h-9 rounded-xl flex items-center justify-center mr-5 flex-shrink-0" style={{ background: '#F5F5F7', color: '#86868B' }}><Ic /></div>
                <div className="flex-1 min-w-0">
                  <div className="text-[10px] font-semibold uppercase tracking-wider mb-0.5" style={{ color: '#86868B' }}>{compLabels[ct]}</div>
                  <div className="text-sm font-medium truncate" style={{ color: '#1D1D1F' }}>{comp.name}</div>
                  {comp.brand && <span className="text-[10px]" style={{ color: '#D2D2D7' }}>{comp.brand}</span>}
                </div>
                <div className="text-sm font-bold mr-6 flex-shrink-0" style={{ color: '#1D1D1F' }}>{formatPrice(comp.price)}</div>
                <div className="flex items-center gap-2 flex-shrink-0">
                  <div className="dot-ok mr-2" />
                  <button onClick={() => checkLivePrice(ct, comp.id)} disabled={priceLoading === ct} className="flex items-center gap-1 text-[11px] font-medium transition-colors px-2 py-1 rounded-md"
                    style={{ color: priceLoading === ct ? '#86868B' : (isSwapping ? '#86868B' : '#0071E3'), background: 'rgba(0,113,227,0.05)' }}>
                    {priceLoading === ct ? <div className="w-3 h-3 rounded-full animate-spin" style={{ border: '1.5px solid #E8E8ED', borderTopColor: '#0071E3' }} /> : <Icons.refresh />}
                    Live
                  </button>
                  <button onClick={() => fetchAlts(ct)} className="text-[11px] font-medium transition-colors px-2 py-1 rounded-md"
                    style={{ color: isSwapping ? '#fff' : '#86868B', background: isSwapping ? '#0071E3' : '#F5F5F7' }}>
                    Swap
                  </button>
                </div>
              </div>

              <AnimatePresence>
                {isSwapping && (
                  <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={ease} className="overflow-hidden"
                    style={{ borderBottom: '1px solid rgba(0,0,0,0.04)', background: '#FAFAFA' }}>
                    <div className="px-6 py-4">
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="text-xs font-semibold" style={{ color: '#1D1D1F' }}>Compatible Alternatives</h4>
                        <button onClick={() => setSwapType(null)} style={{ color: '#86868B' }}><Icons.close /></button>
                      </div>
                      {swapLoading ? (
                        <div className="text-center py-3"><div className="inline-block w-4 h-4 rounded-full animate-spin" style={{ border: '2px solid #E8E8ED', borderTopColor: '#0071E3' }} /><p className="text-xs mt-2" style={{ color: '#86868B' }}>Searching...</p></div>
                      ) : alternatives.length === 0 ? (
                        <p className="text-xs text-center py-3" style={{ color: '#86868B' }}>No compatible alternatives found.</p>
                      ) : (
                        <div className="space-y-1 max-h-52 overflow-y-auto scrollbar-hide">
                          {alternatives.map(alt => {
                            const diff = alt.price - (comp.price || 0);
                            return (
                              <button key={alt.id} onClick={() => selectAlt(ct, alt)} className="w-full flex items-center p-3 rounded-xl text-left transition-all hover:bg-white hover:shadow-sm">
                                <div className="w-7 h-7 rounded-lg flex items-center justify-center mr-3 flex-shrink-0" style={{ background: '#F5F5F7', color: '#86868B' }}><Ic /></div>
                                <div className="flex-1 min-w-0">
                                  <div className="text-xs font-medium truncate" style={{ color: '#1D1D1F' }}>{alt.name}</div>
                                  <div className="text-[10px]" style={{ color: '#86868B' }}>{alt.brand}</div>
                                </div>
                                <div className="text-right ml-3 flex-shrink-0">
                                  <div className="text-xs font-bold" style={{ color: '#1D1D1F' }}>{formatPrice(alt.price)}</div>
                                  <div className="text-[10px] font-medium" style={{ color: diff > 0 ? '#FF3B30' : diff < 0 ? '#34C759' : '#86868B' }}>
                                    {diff > 0 ? `+${formatPrice(diff)}` : diff < 0 ? `-${formatPrice(Math.abs(diff))}` : 'Same'}
                                  </div>
                                </div>
                              </button>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};

// ─── Results Step ────────────────────────────────────────────
const ResultsStep = ({ builds: initialBuilds, budget, usageType, onReset, optimizationInfo }) => {
  const [builds, setBuilds] = useState(initialBuilds);
  const [originalBuilds] = useState(initialBuilds);
  const [isCustomized, setIsCustomized] = useState(false);
  const usageNames = {}; // dynamic names handled in UI

  const handleSwap = (bi, ct, nc) => {
    setBuilds(prev => {
      const u = [...prev]; const b = { ...u[bi] };
      b.components = { ...b.components, [ct]: nc };
      b.total_cost = Object.values(b.components).filter(Boolean).reduce((s, c) => s + (c.price || 0), 0);
      b.budget_utilization = Math.round((b.total_cost / budget) * 1000) / 10;
      const cpu = b.components.cpu; const dGpu = !!b.components.gpu; const iGpu = cpu?.integrated_graphics === true;
      b.is_apu_build = !dGpu && iGpu; b.igpu_name = iGpu ? (cpu.igpu_name || 'Integrated Graphics') : null;
      u[bi] = b; return u;
    });
    setIsCustomized(true);
  };

  const handleUpdatePrice = (bi, ct, newPrice) => {
    setBuilds(prev => {
      const u = [...prev]; const b = { ...u[bi] };
      const oldComp = b.components[ct];
      b.components = { ...b.components, [ct]: { ...oldComp, price: newPrice } };
      b.total_cost = Object.values(b.components).filter(Boolean).reduce((s, c) => s + (c.price || 0), 0);
      b.budget_utilization = Math.round((b.total_cost / budget) * 1000) / 10;
      u[bi] = b; return u;
    });
    setIsCustomized(true);
  };

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={ease} className="space-y-6">
      <div className="text-center mb-2">
        <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ color: '#1D1D1F' }}>Your Builds</h2>
        <p className="text-sm" style={{ color: '#86868B' }}>
          Optimized for <span className="font-medium" style={{ color: '#1D1D1F' }}>{usageType.replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase())}</span> · {formatPrice(budget)} budget
        </p>
      </div>

      {optimizationInfo && (
        <div className="soft-card p-4 flex items-center justify-center gap-6 text-xs">
          <div><span style={{ color: '#86868B' }}>Generations </span><span className="font-bold" style={{ color: '#1D1D1F' }}>{optimizationInfo.generations_run}</span></div>
          <div><span style={{ color: '#86868B' }}>Components </span><span className="font-bold" style={{ color: '#1D1D1F' }}>{Object.values(optimizationInfo.csp_filtered_counts || {}).reduce((a, b) => a + b, 0)}</span></div>
          <div><span style={{ color: '#86868B' }}>Algorithm </span><span className="font-bold" style={{ color: '#1D1D1F' }}>NSGA-II</span></div>
        </div>
      )}

      <div className="space-y-5">
        {builds.map((b, i) => <BuildCard key={i} build={b} index={i} onSwapComponent={handleSwap} onUpdatePrice={handleUpdatePrice} />)}
      </div>

      <div className="text-center pt-4 flex justify-center gap-3">
        {isCustomized && (
          <button onClick={() => { setBuilds(originalBuilds); setIsCustomized(false); }}
            className="px-5 py-2.5 rounded-full text-xs font-medium" style={{ color: '#86868B' }}>↩ Reset All</button>
        )}
        <motion.button onClick={onReset} whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.98 }}
          className="inline-flex items-center gap-2 px-7 py-3 rounded-full text-sm font-semibold" style={{ background: '#0071E3', color: '#fff' }}>
          <Icons.arrowLeft /> New Build
        </motion.button>
      </div>
    </motion.div>
  );
};

// ─── Error ───────────────────────────────────────────────────
const ErrorDisplay = ({ error, onRetry }) => (
  <div className="text-center py-20">
    <div className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4" style={{ background: 'rgba(255,59,48,0.08)', color: '#FF3B30' }}><Icons.close /></div>
    <h3 className="text-lg font-semibold mb-2" style={{ color: '#1D1D1F' }}>Something Went Wrong</h3>
    <p className="text-xs mb-6" style={{ color: '#86868B' }}>{error}</p>
    <button onClick={onRetry} className="px-6 py-2.5 rounded-full text-sm font-medium" style={{ background: '#0071E3', color: '#fff' }}>Try Again</button>
  </div>
);

// ─── Main ────────────────────────────────────────────────────
const SmartWizard = () => {
  const [showLanding, setShowLanding] = useState(true);
  const [step, setStep] = useState(0);
  const [budget, setBudget] = useState(80000);
  const [usageType, setUsageType] = useState('');
  const [cpuBrand, setCpuBrand] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);
  const [optimizationInfo, setOptimizationInfo] = useState(null);
  const API_URL = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '' : 'http://localhost:5000');

  const fetchRecommendations = async () => {
    setLoading(true); setError(null);
    try {
      const r = await fetch(`${API_URL}/api/recommend`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ budget, usage_type: usageType, num_builds: 3, cpu_brand: cpuBrand || undefined }) });
      const d = await r.json();
      if (!r.ok || !d.success) throw new Error(d.error || 'Failed');
      setResults(d.recommendations); setOptimizationInfo(d.optimization_info); setStep(3);
    } catch (e) { setError(e.message); } finally { setLoading(false); }
  };

  const handleNext = () => { if (step === 2) fetchRecommendations(); else setStep(step + 1); };
  const handleReset = () => { setStep(0); setBudget(80000); setUsageType(''); setCpuBrand(''); setResults(null); setError(null); };

  if (showLanding) return <LandingPage onGetStarted={() => setShowLanding(false)} />;

  return (
    <div className="min-h-screen" style={{ background: '#F5F5F7' }}>
      <Header showBack onBack={() => { if (step === 0) setShowLanding(true); else if (!loading) handleReset(); }} />
      <main className="max-w-4xl mx-auto px-6 py-12">
        {!loading && step < 3 && <StepIndicator currentStep={step} steps={['Budget', 'Use Case', 'CPU', 'Results']} />}
        <div className="soft-card p-8">
          <AnimatePresence mode="wait">
            {error ? <ErrorDisplay key="error" error={error} onRetry={handleReset} />
              : loading ? <LoadingStep key="loading" />
                : step === 0 ? <BudgetStep key="budget" budget={budget} setBudget={setBudget} onNext={handleNext} />
                  : step === 1 ? <UsageStep key="usage" usageType={usageType} setUsageType={setUsageType} onNext={handleNext} onBack={() => setStep(0)} />
                    : step === 2 ? <CpuBrandStep key="cpu" cpuBrand={cpuBrand} setCpuBrand={setCpuBrand} onNext={handleNext} onBack={() => setStep(1)} />
                      : results ? <ResultsStep key="results" builds={results} budget={budget} usageType={usageType} onReset={handleReset} optimizationInfo={optimizationInfo} />
                        : null}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
};

export default SmartWizard;
