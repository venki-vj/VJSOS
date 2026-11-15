import "./index.css";
import { VJSOSBroll } from "./VJSOSBroll";
import { Composition } from "remotion";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="VJSOSBroll"
      component={VJSOSBroll}
      durationInFrames={19200}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};