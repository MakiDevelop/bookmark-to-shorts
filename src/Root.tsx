import { Composition } from "remotion";
import { BkmkShort } from "./BkmkShort";
import scenesData from "../data/scenes.json";

const FPS = 30;
const totalDuration = scenesData.total_duration_sec ?? 45;

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="BkmkShort"
      component={BkmkShort}
      durationInFrames={Math.ceil(totalDuration * FPS) + FPS}
      fps={FPS}
      width={1920}
      height={1080}
      defaultProps={{ scenes: scenesData.scenes, title: scenesData.title }}
    />
  );
};
