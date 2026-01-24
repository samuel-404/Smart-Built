import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const Icons = {
  gamepad: () => (
    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
    </svg>
  ),
  video: () => (
    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
    </svg>
  ),
  book: () => (
    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
    </svg>
  ),
  briefcase: () => (
    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
    </svg>
  ),
  cpu: () => (
    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
    </svg>
  ),
  check: () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
    </svg>
  ),
  arrowRight: () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
    </svg>
  ),
  arrowLeft: () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
    </svg>
  ),
  loading: () => (
    <svg className="w-8 h-8 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
    </svg>
  ),
};

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(price);
};

const StepIndicator = ({ currentStep, totalSteps }) => {
  return (
    <div className="flex items-center justify-center mb-8">
      {Array.from({ length: totalSteps }).map((_, index) => (
        <React.Fragment key={index}>
          <motion.div
            initial={{ scale: 0.8 }}
            animate={{ 
              scale: currentStep === index ? 1.1 : 1,
              backgroundColor: currentStep >= index ? '#6366f1' : '#e5e7eb'
            }}
            className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold
              ${currentStep >= index ? 'text-white' : 'text-gray-500'}`}
          >
            {currentStep > index ? <Icons.check /> : index + 1}
          </motion.div>
          {index < totalSteps - 1 && (
            <motion.div
              initial={{ scaleX: 0 }}
              animate={{ 
                scaleX: 1,
                backgroundColor: currentStep > index ? '#6366f1' : '#e5e7eb'
              }}
              className="w-16 h-1 mx-2 origin-left"
            />
          )}
        </React.Fragment>
      ))}
    </div>
  );
};

const BudgetStep = ({ budget, setBudget, onNext }) => {
  const budgetTiers = [
    { min: 35000, max: 50000, label: 'Budget', color: 'green' },
    { min: 50000, max: 80000, label: 'Mid-Range', color: 'blue' },
    { min: 80000, max: 120000, label: 'High-End', color: 'purple' },
    { min: 120000, max: 200000, label: 'Enthusiast', color: 'orange' },
  ];

  const getCurrentTier = () => {
    return budgetTiers.find(tier => budget >= tier.min && budget <= tier.max) || budgetTiers[0];
  };

  const currentTier = getCurrentTier();

  return (
    <motion.div
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      className="space-y-8"
    >
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">What's Your Budget?</h2>
        <p className="text-gray-600">Drag the slider to set your maximum budget in Rupees</p>
      </div>

      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl p-8 text-white">
        <div className="text-center mb-6">
          <motion.div
            key={budget}
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="text-5xl font-bold mb-2"
          >
            {formatPrice(budget)}
          </motion.div>
          <motion.span
            key={currentTier.label}
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="inline-block px-4 py-1 rounded-full text-sm font-medium bg-white/20"
          >
            {currentTier.label} Build
          </motion.span>
        </div>

        <input
          type="range"
          min="35000"
          max="200000"
          step="5000"
          value={budget}
          onChange={(e) => setBudget(parseInt(e.target.value))}
          className="w-full h-3 bg-white/30 rounded-lg appearance-none cursor-pointer
            [&::-webkit-slider-thumb]:appearance-none
            [&::-webkit-slider-thumb]:w-6
            [&::-webkit-slider-thumb]:h-6
            [&::-webkit-slider-thumb]:bg-white
            [&::-webkit-slider-thumb]:rounded-full
            [&::-webkit-slider-thumb]:shadow-lg
            [&::-webkit-slider-thumb]:cursor-pointer"
        />

        <div className="flex justify-between text-sm mt-2 opacity-80">
          <span>₹35,000</span>
          <span>₹2,00,000</span>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-3">
        {budgetTiers.map((tier) => (
          <button
            key={tier.label}
            onClick={() => setBudget(Math.floor((tier.min + tier.max) / 2))}
            className={`p-3 rounded-xl text-center transition-all ${
              currentTier.label === tier.label
                ? 'bg-indigo-100 border-2 border-indigo-500'
                : 'bg-gray-100 border-2 border-transparent hover:bg-gray-200'
            }`}
          >
            <div className="text-sm font-medium text-gray-900">{tier.label}</div>
            <div className="text-xs text-gray-500">
              {formatPrice(tier.min)} - {formatPrice(tier.max)}
            </div>
          </button>
        ))}
      </div>

      <div className="flex justify-end">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={onNext}
          className="flex items-center gap-2 bg-indigo-600 text-white px-8 py-3 rounded-xl font-medium
            hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-500/30"
        >
          Continue
          <Icons.arrowRight />
        </motion.button>
      </div>
    </motion.div>
  );
};

const UsageStep = ({ usageType, setUsageType, onNext, onBack }) => {
  const usageTypes = [
    {
      id: 'gaming',
      name: 'Gaming',
      icon: Icons.gamepad,
      description: 'High FPS gaming at 1080p/1440p with ray tracing support',
      color: 'from-purple-500 to-pink-500',
    },
    {
      id: 'content_creation',
      name: 'Content Creation',
      icon: Icons.video,
      description: 'Video editing, 3D rendering, and creative workflows',
      color: 'from-blue-500 to-cyan-500',
    },
    {
      id: 'student',
      name: 'Student / General',
      icon: Icons.book,
      description: 'Coding, office work, light gaming, and everyday tasks',
      color: 'from-green-500 to-emerald-500',
    },
    {
      id: 'workstation',
      name: 'Workstation',
      icon: Icons.briefcase,
      description: 'Professional CAD, simulation, and heavy computational work',
      color: 'from-orange-500 to-red-500',
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      className="space-y-8"
    >
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">What Will You Use It For?</h2>
        <p className="text-gray-600">Select your primary use case to optimize component selection</p>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {usageTypes.map((type) => (
          <motion.button
            key={type.id}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setUsageType(type.id)}
            className={`relative p-6 rounded-2xl text-left transition-all overflow-hidden ${
              usageType === type.id
                ? 'ring-4 ring-indigo-500 ring-offset-2'
                : 'hover:shadow-lg'
            }`}
          >
            <div className={`absolute inset-0 bg-gradient-to-br ${type.color} opacity-10`} />
            <div className="relative">
              <div className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${type.color} text-white mb-4`}>
                <type.icon />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-1">{type.name}</h3>
              <p className="text-sm text-gray-600">{type.description}</p>
              {usageType === type.id && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute top-4 right-4 w-6 h-6 bg-indigo-600 rounded-full flex items-center justify-center text-white"
                >
                  <Icons.check />
                </motion.div>
              )}
            </div>
          </motion.button>
        ))}
      </div>

      <div className="flex justify-between">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={onBack}
          className="flex items-center gap-2 bg-gray-100 text-gray-700 px-6 py-3 rounded-xl font-medium
            hover:bg-gray-200 transition-colors"
        >
          <Icons.arrowLeft />
          Back
        </motion.button>
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={onNext}
          disabled={!usageType}
          className="flex items-center gap-2 bg-indigo-600 text-white px-8 py-3 rounded-xl font-medium
            hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-500/30
            disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Generate Builds
          <Icons.arrowRight />
        </motion.button>
      </div>
    </motion.div>
  );
};

const LoadingStep = () => {
  const messages = [
    'Analyzing component compatibility...',
    'Running AC-3 constraint propagation...',
    'Initializing genetic algorithm...',
    'Evolving optimal configurations...',
    'Calculating Pareto-optimal front...',
    'Finalizing recommendations...',
  ];

  const [messageIndex, setMessageIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % messages.length);
    }, 1500);
    return () => clearInterval(interval);
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="flex flex-col items-center justify-center py-16"
    >
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
        className="text-indigo-600 mb-8"
      >
        <Icons.loading />
      </motion.div>
      
      <div className="relative h-8 overflow-hidden">
        <AnimatePresence mode="wait">
          <motion.p
            key={messageIndex}
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: -20, opacity: 0 }}
            className="text-gray-600 text-center"
          >
            {messages[messageIndex]}
          </motion.p>
        </AnimatePresence>
      </div>

      <div className="w-64 h-2 bg-gray-200 rounded-full mt-8 overflow-hidden">
        <motion.div
          initial={{ width: '0%' }}
          animate={{ width: '100%' }}
          transition={{ duration: 8, ease: 'easeInOut' }}
          className="h-full bg-gradient-to-r from-indigo-500 to-purple-500"
        />
      </div>
    </motion.div>
  );
};

const BuildCard = ({ build, index }) => {
  const [expanded, setExpanded] = useState(false);

  const getLabelColor = (label) => {
    if (label.includes('Performance')) return 'from-purple-500 to-pink-500';
    if (label.includes('Value')) return 'from-green-500 to-emerald-500';
    if (label.includes('Budget')) return 'from-blue-500 to-cyan-500';
    return 'from-gray-500 to-gray-600';
  };

  const componentOrder = ['cpu', 'gpu', 'motherboard', 'ram', 'storage', 'psu', 'case'];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100"
    >
      <div className={`bg-gradient-to-r ${getLabelColor(build.label)} p-6 text-white`}>
        <div className="flex justify-between items-start">
          <div>
            <span className="inline-block px-3 py-1 bg-white/20 rounded-full text-sm mb-2">
              #{index + 1} Recommended
            </span>
            <h3 className="text-2xl font-bold">{build.label}</h3>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold">{formatPrice(build.total_cost)}</div>
            <div className="text-sm opacity-80">
              {build.budget_utilization}% of budget
            </div>
          </div>
        </div>
        
        <div className="mt-4 flex gap-4">
          <div className="bg-white/20 rounded-lg px-4 py-2">
            <div className="text-sm opacity-80">Performance</div>
            <div className="text-xl font-bold">{build.performance_score}</div>
          </div>
          <div className={`rounded-lg px-4 py-2 ${build.within_budget ? 'bg-green-500/30' : 'bg-red-500/30'}`}>
            <div className="text-sm opacity-80">Budget Status</div>
            <div className="text-xl font-bold">{build.within_budget ? '✓ Within' : '⚠ Over'}</div>
          </div>
        </div>
      </div>

      <div className="p-6">
        <div className="space-y-3">
          {componentOrder.map((compType) => {
            const comp = build.components[compType];
            if (!comp) return null;
            
            return (
              <div
                key={compType}
                className="flex justify-between items-center p-3 bg-gray-50 rounded-xl"
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center text-indigo-600">
                    <Icons.cpu />
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 uppercase font-medium">{compType}</div>
                    <div className="font-medium text-gray-900">{comp.name}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-semibold text-gray-900">{formatPrice(comp.price)}</div>
                  <div className="text-xs text-gray-500">Score: {comp.performance_score}</div>
                </div>
              </div>
            );
          })}
        </div>

        <button
          onClick={() => setExpanded(!expanded)}
          className="w-full mt-4 py-3 bg-gray-100 rounded-xl text-gray-700 font-medium
            hover:bg-gray-200 transition-colors"
        >
          {expanded ? 'Hide Details' : 'Show Full Specs'}
        </button>

        <AnimatePresence>
          {expanded && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="overflow-hidden"
            >
              <div className="pt-4 space-y-4">
                {componentOrder.map((compType) => {
                  const comp = build.components[compType];
                  if (!comp) return null;

                  return (
                    <div key={`details-${compType}`} className="text-sm">
                      <h4 className="font-semibold text-gray-900 mb-2">{compType.toUpperCase()} Details</h4>
                      <div className="grid grid-cols-2 gap-2 text-gray-600">
                        {Object.entries(comp).map(([key, value]) => {
                          if (['id', 'name', 'price', 'performance_score', 'brand'].includes(key)) return null;
                          return (
                            <div key={key} className="flex justify-between bg-gray-50 px-2 py-1 rounded">
                              <span className="capitalize">{key.replace(/_/g, ' ')}:</span>
                              <span className="font-medium">{String(value)}</span>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  );
                })}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

const ResultsStep = ({ builds, budget, usageType, onReset, optimizationInfo }) => {
  const usageNames = {
    gaming: 'Gaming',
    content_creation: 'Content Creation',
    student: 'Student / General',
    workstation: 'Workstation',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-8"
    >
      <div className="text-center">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4"
        >
          <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </motion.div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Your Perfect Builds</h2>
        <p className="text-gray-600">
          Optimized for {usageNames[usageType]} with a budget of {formatPrice(budget)}
        </p>
      </div>

      {optimizationInfo && (
        <div className="bg-indigo-50 rounded-xl p-4">
          <h4 className="font-semibold text-indigo-900 mb-2">AI Optimization Details</h4>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-indigo-600">Generations:</span>
              <span className="ml-2 font-medium">{optimizationInfo.generations_run}</span>
            </div>
            <div>
              <span className="text-indigo-600">Components Analyzed:</span>
              <span className="ml-2 font-medium">
                {Object.values(optimizationInfo.csp_filtered_counts || {}).reduce((a, b) => a + b, 0)}
              </span>
            </div>
            <div>
              <span className="text-indigo-600">Algorithm:</span>
              <span className="ml-2 font-medium">NSGA-II + AC-3</span>
            </div>
          </div>
        </div>
      )}

      <div className="space-y-6">
        {builds.map((build, index) => (
          <BuildCard key={index} build={build} index={index} />
        ))}
      </div>

      <div className="flex justify-center gap-4">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={onReset}
          className="flex items-center gap-2 bg-indigo-600 text-white px-8 py-3 rounded-xl font-medium
            hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-500/30"
        >
          <Icons.arrowLeft />
          Start Over
        </motion.button>
      </div>
    </motion.div>
  );
};

const ErrorDisplay = ({ error, onRetry }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="text-center py-16"
    >
      <div className="inline-flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mb-4">
        <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </div>
      <h3 className="text-xl font-bold text-gray-900 mb-2">Oops! Something went wrong</h3>
      <p className="text-gray-600 mb-6">{error}</p>
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={onRetry}
        className="bg-indigo-600 text-white px-6 py-3 rounded-xl font-medium hover:bg-indigo-700 transition-colors"
      >
        Try Again
      </motion.button>
    </motion.div>
  );
};

const SmartWizard = () => {
  const [step, setStep] = useState(0);
  const [budget, setBudget] = useState(80000);
  const [usageType, setUsageType] = useState('gaming');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);
  const [optimizationInfo, setOptimizationInfo] = useState(null);

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

  const fetchRecommendations = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/api/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          budget: budget,
          usage_type: usageType,
          num_builds: 3,
        }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Failed to get recommendations');
      }

      setResults(data.recommendations);
      setOptimizationInfo(data.optimization_info);
      setStep(3);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleNext = () => {
    if (step === 1) {
      setStep(2);
      fetchRecommendations();
    } else {
      setStep(step + 1);
    }
  };

  const handleBack = () => {
    setStep(step - 1);
  };

  const handleReset = () => {
    setStep(0);
    setBudget(80000);
    setUsageType('gaming');
    setResults(null);
    setError(null);
    setOptimizationInfo(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
            SmartBuild
          </h1>
          <p className="text-gray-600 mt-2">Intelligent PC Configuration Consultant</p>
        </motion.div>

        {step < 3 && !loading && <StepIndicator currentStep={step} totalSteps={3} />}

        <motion.div
          layout
          className="bg-white rounded-3xl shadow-xl p-8"
        >
          <AnimatePresence mode="wait">
            {error ? (
              <ErrorDisplay key="error" error={error} onRetry={handleReset} />
            ) : loading ? (
              <LoadingStep key="loading" />
            ) : step === 0 ? (
              <BudgetStep
                key="budget"
                budget={budget}
                setBudget={setBudget}
                onNext={handleNext}
              />
            ) : step === 1 ? (
              <UsageStep
                key="usage"
                usageType={usageType}
                setUsageType={setUsageType}
                onNext={handleNext}
                onBack={handleBack}
              />
            ) : step === 3 && results ? (
              <ResultsStep
                key="results"
                builds={results}
                budget={budget}
                usageType={usageType}
                onReset={handleReset}
                optimizationInfo={optimizationInfo}
              />
            ) : null}
          </AnimatePresence>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="text-center mt-8 text-gray-500 text-sm"
        >
          Powered by Hybrid AI: CSP (AC-3) + NSGA-II Genetic Algorithm
        </motion.div>
      </div>
    </div>
  );
};

export default SmartWizard;
