import {
  AbsoluteFill,
  Audio,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Easing,
} from "remotion";

interface Scene {
  id: number;
  narration: string;
  visual_hint: string;
  audio_file: string;
  audio_duration_sec: number;
}

interface Props {
  scenes: Scene[];
  title: string;
}

const PALETTES = [
  { accent: "#6C5CE7", glow: "#a29bfe", bg: "#1a1625" },
  { accent: "#00B894", glow: "#55efc4", bg: "#0d261e" },
  { accent: "#E17055", glow: "#fab1a0", bg: "#2d1a14" },
  { accent: "#0984E3", glow: "#74b9ff", bg: "#0c1929" },
];

const GridBackground: React.FC<{ color: string; frame: number }> = ({
  color,
  frame,
}) => {
  const drift = frame * 0.3;
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        opacity: 0.08,
        backgroundImage: `
          linear-gradient(${color} 1px, transparent 1px),
          linear-gradient(90deg, ${color} 1px, transparent 1px)
        `,
        backgroundSize: "60px 60px",
        backgroundPosition: `${drift}px ${drift}px`,
      }}
    />
  );
};

const GlowOrb: React.FC<{
  x: number;
  y: number;
  size: number;
  color: string;
  frame: number;
  delay: number;
}> = ({ x, y, size, color, frame, delay }) => {
  const pulse = Math.sin((frame + delay) * 0.04) * 0.3 + 0.7;
  const floatY = Math.sin((frame + delay) * 0.02) * 15;
  return (
    <div
      style={{
        position: "absolute",
        left: `${x}%`,
        top: `${y}%`,
        width: size,
        height: size,
        borderRadius: "50%",
        background: `radial-gradient(circle, ${color}66 0%, transparent 70%)`,
        opacity: pulse,
        transform: `translateY(${floatY}px)`,
        filter: `blur(${size * 0.3}px)`,
      }}
    />
  );
};

const SceneCard: React.FC<{
  scene: Scene;
  palette: (typeof PALETTES)[0];
  index: number;
}> = ({ scene, palette, index }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 12, stiffness: 80 } });
  const numberSlide = spring({ frame, fps, config: { damping: 20, stiffness: 100 } });

  const totalChars = scene.narration.length;
  const revealedChars = Math.floor(
    interpolate(frame, [8, Math.min(fps * 2.5, scene.audio_duration_sec * fps * 0.7)], [0, totalChars], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.quad),
    })
  );

  const hintOpacity = interpolate(
    frame,
    [scene.audio_duration_sec * fps * 0.4, scene.audio_duration_sec * fps * 0.55],
    [0, 0.8],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const audioPath = `scene-${scene.id}.mp3`;
  const sceneNum = String(index + 1).padStart(2, "0");

  return (
    <AbsoluteFill style={{ background: palette.bg }}>
      <Audio src={staticFile(audioPath)} />

      <GridBackground color={palette.accent} frame={frame} />

      <GlowOrb x={75} y={20} size={300} color={palette.glow} frame={frame} delay={0} />
      <GlowOrb x={15} y={70} size={200} color={palette.accent} frame={frame} delay={50} />
      <GlowOrb x={85} y={75} size={150} color={palette.glow} frame={frame} delay={100} />

      {/* Large scene number - left side */}
      <div
        style={{
          position: "absolute",
          left: 60,
          top: "50%",
          transform: `translateY(-50%) translateX(${interpolate(numberSlide, [0, 1], [-120, 0])}px)`,
          fontSize: 280,
          fontWeight: 900,
          color: `${palette.accent}15`,
          fontFamily: "system-ui, -apple-system, sans-serif",
          lineHeight: 1,
          letterSpacing: -10,
        }}
      >
        {sceneNum}
      </div>

      {/* Accent vertical bar */}
      <div
        style={{
          position: "absolute",
          left: 180,
          top: "25%",
          width: 4,
          height: `${interpolate(entrance, [0, 1], [0, 50])}%`,
          background: `linear-gradient(to bottom, ${palette.accent}, transparent)`,
          borderRadius: 2,
        }}
      />

      {/* Scene counter */}
      <div
        style={{
          position: "absolute",
          top: 50,
          right: 60,
          fontSize: 20,
          color: `${palette.accent}88`,
          fontFamily: "monospace",
          opacity: entrance,
          letterSpacing: 6,
        }}
      >
        {sceneNum} / 04
      </div>

      {/* Main narration - typewriter effect */}
      <div
        style={{
          position: "absolute",
          left: 220,
          top: "22%",
          right: 100,
          fontSize: 52,
          color: "#FAFAFA",
          fontWeight: 700,
          lineHeight: 1.7,
          fontFamily: "system-ui, -apple-system, sans-serif",
        }}
      >
        <span>{scene.narration.slice(0, revealedChars)}</span>
        <span
          style={{
            display: revealedChars < totalChars ? "inline-block" : "none",
            width: 3,
            height: 52,
            backgroundColor: palette.accent,
            marginLeft: 4,
            opacity: Math.sin(frame * 0.15) > 0 ? 1 : 0,
            verticalAlign: "middle",
          }}
        />
      </div>

      {/* Visual hint - bottom area */}
      <div
        style={{
          position: "absolute",
          bottom: 120,
          left: 220,
          right: 100,
          fontSize: 22,
          color: `${palette.glow}`,
          opacity: hintOpacity,
          fontStyle: "italic",
          letterSpacing: 1,
          borderLeft: `3px solid ${palette.accent}44`,
          paddingLeft: 16,
        }}
      >
        {scene.visual_hint}
      </div>

      {/* Progress bar - bottom */}
      <div
        style={{
          position: "absolute",
          bottom: 50,
          left: 60,
          right: 60,
          height: 3,
          backgroundColor: `${palette.accent}22`,
          borderRadius: 2,
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${interpolate(frame, [0, scene.audio_duration_sec * fps], [0, 100], { extrapolateRight: "clamp" })}%`,
            background: `linear-gradient(90deg, ${palette.accent}, ${palette.glow})`,
            borderRadius: 2,
            boxShadow: `0 0 12px ${palette.accent}66`,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

const TitleCard: React.FC<{ title: string }> = ({ title }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleEntrance = spring({ frame, fps, config: { damping: 15, stiffness: 60 } });
  const subtitleEntrance = spring({
    frame: Math.max(0, frame - 10),
    fps,
    config: { damping: 15, stiffness: 60 },
  });
  const lineWidth = interpolate(frame, [5, 25], [0, 400], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
  });

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(135deg, #0a0a12 0%, #1a1a2e 40%, #16213e 100%)",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <GlowOrb x={50} y={30} size={500} color="#6C5CE7" frame={frame} delay={0} />
      <GlowOrb x={30} y={60} size={300} color="#0984E3" frame={frame} delay={30} />
      <GlowOrb x={70} y={70} size={250} color="#00B894" frame={frame} delay={60} />

      <GridBackground color="#6C5CE7" frame={frame} />

      <div
        style={{
          transform: `translateY(${interpolate(titleEntrance, [0, 1], [60, 0])}px)`,
          opacity: titleEntrance,
          textAlign: "center",
        }}
      >
        <div
          style={{
            fontSize: 88,
            color: "#FAFAFA",
            fontWeight: 900,
            letterSpacing: 4,
            fontFamily: "system-ui, -apple-system, sans-serif",
            textShadow: "0 0 60px rgba(108, 92, 231, 0.4)",
          }}
        >
          {title}
        </div>

        <div
          style={{
            width: lineWidth,
            height: 3,
            background: "linear-gradient(90deg, transparent, #6C5CE7, transparent)",
            margin: "24px auto",
          }}
        />

        <div
          style={{
            fontSize: 26,
            color: "#888",
            fontFamily: "monospace",
            opacity: subtitleEntrance,
            letterSpacing: 8,
          }}
        >
          MK-BRAIN WEEKLY
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const BkmkShort: React.FC<Props> = ({ scenes, title }) => {
  const { fps } = useVideoConfig();

  const sequenceData: Array<{
    from: number;
    dur: number;
    scene: Scene;
    index: number;
  }> = [];
  let cumulativeFrames = fps;
  for (let i = 0; i < scenes.length; i++) {
    const dur = Math.ceil(scenes[i].audio_duration_sec * fps);
    sequenceData.push({
      from: cumulativeFrames,
      dur,
      scene: scenes[i],
      index: i,
    });
    cumulativeFrames += dur;
  }

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a0a" }}>
      <Sequence from={0} durationInFrames={fps}>
        <TitleCard title={title} />
      </Sequence>

      {sequenceData.map(({ from, dur, scene, index }) => (
        <Sequence key={scene.id} from={from} durationInFrames={dur}>
          <SceneCard
            scene={scene}
            palette={PALETTES[index % PALETTES.length]}
            index={index}
          />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
