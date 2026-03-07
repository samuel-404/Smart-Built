import fs from 'fs';

const filePath = 'frontend/src/components/SmartWizard.jsx';
let content = fs.readFileSync(filePath, 'utf8');

// Define the new usage groups
const newUsageGroupsCode = `
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
    if(found) selectedItemName = found.name;
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
              style={{ border: hasSelected ? \`1.5px solid \${g.color}\` : '1.5px solid transparent' }}>
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
`

// Replace the UsageStep definition
const startIdx = content.indexOf('const UsageStep = ({ usageType, setUsageType, onNext, onBack }) => {');
const endIdx = content.indexOf('const CpuBrandStep =', startIdx);

if (startIdx !== -1 && endIdx !== -1) {
    const newContent = content.substring(0, startIdx) +
        "const UsageStep = ({ usageType, setUsageType, onNext, onBack }) => {" +
        newUsageGroupsCode +
        "// ─── CPU Brand Step " + content.substring(endIdx + 20); // The +20 skips "const CpuBrandStep =" to align with the rest of the string

    // Actually wait, let's substitute cleanly:
    const replacement = "const UsageStep = ({ usageType, setUsageType, onNext, onBack }) => {" + newUsageGroupsCode + "};\n\n";
    const cleanedContent = content.substring(0, startIdx) + replacement + content.substring(endIdx - 11);

    fs.writeFileSync(filePath, cleanedContent);
    console.log("Replaced UsageStep component.");
} else {
    console.log("Could not find start or end index.");
}

// Since usageNames is used in ResultsStep, let's also fix ResultsStep to handle arbitrary IDs, 
// or at least not crash if it doesn't recognize the name.
// Update ResultsStep usageNames line
content = fs.readFileSync(filePath, 'utf8');
const resultsStart = content.indexOf("const usageNames = { gaming: 'Gaming', content_creation: 'Content Creation'");
if (resultsStart !== -1) {
    const newline = content.indexOf(';', resultsStart);
    content = content.substring(0, resultsStart) + "const usageNames = {}; // dynamic names handled in UI" + content.substring(newline + 1);
    content = content.replace(
        /{usageNames\[usageType\]}/g,
        "{usageType.replace('_', ' ').replace(/\\b\\w/g, c => c.toUpperCase())}"
    );
    fs.writeFileSync(filePath, content);
    console.log("Fixed usageNames mapping in ResultsStep.");
}

