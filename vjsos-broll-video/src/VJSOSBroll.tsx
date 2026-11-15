import {
  AbsoluteFill,
  interpolate,
  Series,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import React from "react";

export const VJSOSBroll: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1e1e2e",
        color: "#ffffff",
        fontFamily: "monospace",
        overflow: "hidden",
      }}
    >
      {/* Dark terminal background with grid */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `
            linear-gradient(rgba(45, 45, 61, 0.3) 1px, transparent 1px),
            linear-gradient(90deg, rgba(45, 45, 61, 0.3) 1px, transparent 1px)
          `,
          backgroundSize: "24px 24px",
          opacity: 0.5,
        }}
      />
      <Series>
        {/* Sequence 1: Cold Open (0:00 - 0:45) */}
        <Series.Sequence durationInFrames={1350}>
          <ColdOpen />
        </Series.Sequence>

        {/* Sequence 2: Architecture Overview (0:45 - 1:45) */}
        <Series.Sequence durationInFrames={1800}>
          <ArchitectureOverview />
        </Series.Sequence>

        {/* Sequence 3: Skill Registry (1:45 - 3:30) */}
        <Series.Sequence durationInFrames={2850}>
          <SkillRegistry />
        </Series.Sequence>

        {/* Sequence 4: Plugin Manager (3:30 - 5:15) */}
        <Series.Sequence durationInFrames={2250}>
          <PluginManager />
        </Series.Sequence>

        {/* Sequence 5: Message Bus (5:15 - 6:45) */}
        <Series.Sequence durationInFrames={2250}>
          <MessageBus />
        </Series.Sequence>

        {/* Sequence 6: Analytics Engine (6:45 - 9:00) */}
        <Series.Sequence durationInFrames={3450}>
          <AnalyticsEngine />
        </Series.Sequence>

        {/* Sequence 7: Learning Engine (9:00 - 11:00) */}
        <Series.Sequence durationInFrames={3000}>
          <LearningEngine />
        </Series.Sequence>

        {/* Sequence 8: Integration Test (11:00 - 12:30) */}
        <Series.Sequence durationInFrames={1350}>
          <IntegrationTest />
        </Series.Sequence>

        {/* Sequence 9: Closing / CTA (12:30 - 13:30) */}
        <Series.Sequence durationInFrames={900}>
          <Closing />
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};

// Sequence 1: Cold Open
export const ColdOpen: React.FC = () => {
  return (
    <>
      <TerminalWindow
        title="cold-open"
        width={880}
        height={480}
        left={220}
        top={300}
        startFrame={0}
      >
        <TerminalLine text="$ git log --oneline -5" delayFrames={30} />
        <TerminalOutput
          lines={[
            "2a7f1c3 feat: add phase 2 integration test suite",
            "b1d3e4f feat: learning engine pattern detection",
            "c98a2d1 feat: analytics engine cost tracking",
            "d4f5b6e feat: message bus event types",
            "a1b2c3d feat: plugin manifest system",
          ]}
          startFrame={120}
          perLineDelay={20}
        />
        <TerminalLine text="$ cat docs/IMPLEMENTATION_PLAN.md | grep -A2 Phase 2" delayFrames={350} />
        <TerminalOutput
          lines={["Phase 2: Integration [x]", "[x] Skill Registry", "[x] Plugin Manager"]}
          startFrame={470}
          perLineDelay={20}
        />
      </TerminalWindow>
      <TitleCard
        title="VJSOS-AI PHASE 2"
        subtitle="Integration Walkthrough"
        startFrame={750}
        duration={500}
      />
    </>
  );
};

// Sequence 2: Architecture Overview
export const ArchitectureOverview: React.FC = () => {
  return (
    <>
      <ArchitectureDiagram startFrame={0} duration={1800} />
      <SectionTitle
        title="ARCHITECTURE OVERVIEW"
        startFrame={200}
        duration={150}
      />
      <TerminalWindow
        title="vjsos-ai"
        width={800}
        height={400}
        left={340}
        top={360}
        startFrame={500}
        duration={1200}
      >
        <TerminalLine text="$ tree -L 3 skills plugins analytics learning kernel" delayFrames={50} />
        <TerminalOutput
          lines={[
            "skills/",
            "├── engineering/",
            "│   ├── android_development/",
            "│   │   ├── skill.md",
            "│   │   └── tests.yml",
            "│   └── web_frontend/",
            "plugins/",
            "├── github_integration/",
            "├── slack_bot/",
            "analytics/",
            "├── engine/",
            "├── metrics/",
            "learning/",
            "├── patterns/",
            "├── proposals/",
            "kernel/",
            "├── event_bus/",
            "├── governance/",
          ]}
          startFrame={200}
          perLineDelay={15}
        />
      </TerminalWindow>
    </>
  );
};

// Sequence 3: Skill Registry
export const SkillRegistry: React.FC = () => {
  return (
    <>
      <SectionTitle
        title="SKILL REGISTRY"
        startFrame={0}
        duration={150}
      />
      <TerminalWindow
        title="skills-cli"
        width={720}
        height={320}
        left={420}
        top={260}
        startFrame={150}
        duration={2700}
      >
        <TerminalLine text="$ skills list" delayFrames={40} />
        <TerminalOutput
          lines={[
            "🟢 android_development  v1.2.0  engineering",
            "🟢 web_frontend         v2.0.1  engineering",
            "🟡 code_review         v0.9.3  engineering  (testing)",
            "🟢 content_creation    v1.0.0  media",
            "🟢 data_analysis       v1.5.2  research",
          ]}
          startFrame={200}
          perLineDelay={25}
        />
        <TerminalLine
          text={`$ skills prompt android_development --variables task="build login screen"`}
          delayFrames={500}
        />
        <TerminalOutput
          lines={[
            "Rendering template: android_development",
            "Variables applied:",
            "  task → build login screen",
            "  platform → android",
            "",
            "You are an Android development expert.",
            "Task: build login screen",
            "Requirements: Material Design 3, Jetpack Compose...",
            "",
            "✅ Prompt rendered successfully (342ms)",
          ]}
          startFrame={900}
          perLineDelay={20}
        />
      </TerminalWindow>
      <JsonCallout
        data={{
          skill_id: "android_development",
          version: "1.2.0",
          type: "agent_task",
          domain: "engineering",
          qa_status: "verified",
        }}
        startFrame={1500}
        duration={1000}
        position={{ top: 200, right: 40 }}
      />
    </>
  );
};

// Sequence 4: Plugin Manager
export const PluginManager: React.FC = () => {
  return (
    <>
      <SectionTitle
        title="PLUGIN MANAGER"
        startFrame={0}
        duration={150}
      />
      <TerminalWindow
        title="plugins-cli"
        width={720}
        height={360}
        left={420}
        top={220}
        startFrame={150}
        duration={2100}
      >
        <TerminalLine text="$ plugins install github_integration --manifest" delayFrames={40} />
        <TerminalOutput
          lines={["✓ Plugin manifest loaded", "✓ Auth schema: OAuth2", "✓ Rate limit: 5000/hr"]}
          startFrame={200}
          perLineDelay={20}
        />
        <TerminalLine text="$ plugins enable github_integration" delayFrames={600} />
        <TerminalOutput
          lines={["✓ github_integration enabled", "✓ Subscriber registered on MessageBus"]}
          startFrame={800}
          perLineDelay={25}
        />
        <TerminalLine
          text={`$ plugins get github_integration --json | jq .manifest.capabilities`}
          delayFrames={1500}
        />
        <TerminalOutput
          lines={[`["repo.read", "repo.write", "pull_request.create"]`]}
          startFrame={1700}
          perLineDelay={20}
        />
      </TerminalWindow>
      <TealAccentLine x1={300} x2={500} y={320} startFrame={1000} duration={800} />
    </>
  );
};

// Sequence 5: Message Bus
export const MessageBus: React.FC = () => {
  return (
    <>
      <SectionTitle
        title="MESSAGE BUS"
        startFrame={0}
        duration={150}
      />
      <div style={{ display: "flex", gap: "32px", justifyContent: "center", marginTop: "60px" }}>
        <TerminalWindow
          title="publisher"
          width={420}
          height={400}
          left={150}
          top={220}
          startFrame={150}
          duration={1800}
        >
          <TerminalLine
            text={`>>> await bus.publish(Message(type=MessageType.TASK_REQUEST,`}
            delayFrames={60}
          />
          <TerminalLine
            text={`    correlation_id="demo-1",`}
            delayFrames={40}
          />
          <TerminalLine text="    sender='orchestrator'," />
          <TerminalLine text="    payload={'task': 'build_apk'})" />
          <TerminalOutput
            lines={["✓ Message published: TASK_REQUEST (corr=demo-1)"]}
            startFrame={600}
            perLineDelay={30}
          />
        </TerminalWindow>
        <TerminalWindow
          title="subscriber"
          width={420}
          height={400}
          left={600}
          top={220}
          startFrame={600}
          duration={1200}
        >
          <TerminalOutput
            lines={[
              "<< Received TASK_REQUEST >>",
              "  corr=demo-1",
              "  from=orchestrator",
              "  payload={'task': 'build_apk'}",
              "",
              "  → Routing to: android-agent",
              "  ✓ Handler dispatched",
            ]}
            startFrame={100}
            perLineDelay={35}
          />
        </TerminalWindow>
      </div>
      <div style={{ position: "absolute", bottom: "120px", left: "50%", transform: "translateX(-50%)" }}>
        <div style={{ fontSize: "18px", color: "#98c379" }}>
          Message Bus routing: TASK_REQUEST → SubscriberManager → Handler
        </div>
      </div>
    </>
  );
};

// Sequence 6: Analytics Engine
export const AnalyticsEngine: React.FC = () => {
  return (
    <>
      <SectionTitle
        title="ANALYTICS ENGINE"
        startFrame={0}
        duration={150}
      />
      <TerminalWindow
        title="analytics-cli"
        width={720}
        height={420}
        left={420}
        top={220}
        startFrame={150}
        duration={3300}
      >
        <TerminalLine
          text={`$ python -c "from analytics import AnalyticsEngine, DashboardGenerator"`}
          delayFrames={50}
        />
        <TerminalLine text="..." delayFrames={20} />
        <TerminalOutput
          lines={[
            "",
            "📊 Analytics Engine Summary",
            "  Total Tasks: 142",
            "  Completion Rate: 98.2%",
            "  Avg Duration: 4.2s",
            "  Active Agents: 8",
            "  Departments: 3",
            "",
            "💰 Cost Tracking (24h):",
            "  Claude 3.5 Sonnet: $12.34",
            "  Claude 3.5 Haiku: $3.21",
            "",
            "⚠️  Alerts:",
            "  CRITICAL: high_latency (duration > 10s) - 2h cooldown",
            "",
            "📈 Dashboard: dep-eng-dashboard-2026-08-07",
            "  ID: 64a1b2c3",
          ]}
          startFrame={400}
          perLineDelay={25}
        />
      </TerminalWindow>
      <DashboardMetrics startFrame={1800} duration={1500} />
    </>
  );
};

// Sequence 7: Learning Engine
export const LearningEngine: React.FC = () => {
  return (
    <>
      <SectionTitle
        title="LEARNING ENGINE"
        startFrame={0}
        duration={150}
      />
      <TerminalWindow
        title="learning-cli"
        width={800}
        height={420}
        left={340}
        top={200}
        startFrame={150}
        duration={2850}
      >
        <TerminalLine
          text={`$ python -c "from learning import LearningEngine, PatternDetector"`}
          delayFrames={50}
        />
        <TerminalOutput
          lines={[
            "  ✓ Patterns detected: 2",
            "    • PERFORMANCE_DEGRADATION (confidence: 87%)",
            "      - Affected: android_build_tasks",
            "      - Recommendation: Increase timeout threshold",
            "    • RECURRING_FAILURE (confidence: 91%)",
            "      - Affected: web_frontend_skills",
            "      - Recommendation: Review test suite coverage",
          ]}
          startFrame={300}
          perLineDelay={30}
        />
        <TerminalLine
          text={`$ python -c "from learning import ProposalWorkflow"`}
          delayFrames={900}
        />
        <TerminalOutput
          lines={[
            "  Proposal: Fix android timeout issues",
            "  Type: PROCESS_CHANGE",
            "  Priority: HIGH",
            "  Status: SUBMITTED → IN_REVIEW → APPROVED",
            "  Governor: governor@vjsos-ai",
            "",
            "  ✓ Closed loop: Registry reconfigured",
          ]}
          startFrame={1300}
          perLineDelay={25}
        />
      </TerminalWindow>
      <div
        style={{
          position: "absolute",
          top: "380px",
          left: "50%",
          transform: "translateX(-50%)",
          fontSize: "16px",
          color: "#e5c07b",
        }}
      >
        Analytics → Learning → Proposal → Governor → Reconfiguration
      </div>
    </>
  );
};

// Sequence 8: Integration Test
export const IntegrationTest: React.FC = () => {
  return (
    <>
      <SectionTitle
        title="END-TO-END INTEGRATION TEST"
        startFrame={0}
        duration={150}
      />
      <TerminalWindow
        title="test_phase2_integration.py"
        width={920}
        height={520}
        left={180}
        top={180}
        startFrame={150}
        duration={1200}
      >
        <TerminalLine
          text="$ python tests/test_phase2_integration.py"
          delayFrames={50}
        />
        <TerminalOutput
          lines={[
            "Running Phase 2 Integration Test Suite",
            "========================================",
            "",
            "Test Suite 1/6: Skill Registry",
            "  ✓ Registering skill...",
            "  ✓ Loading skill...",
            "  ✓ Testing skill...",
            "  ✓ Prompt rendering...",
            "  PASSED (342ms)",
            "",
            "Test Suite 2/6: Plugin Manager",
            "  ✓ Installing plugin...",
            "  ✓ Enabling plugin...",
            "  ✓ Vault credential storage...",
            "  ✓ Governor approval flow...",
            "  PASSED (1.2s)",
            "",
            "Test Suite 3/6: Message Bus",
            "  ✓ Publishing message...",
            "  ✓ Routing to subscriber...",
            "  ✓ Correlation ID trace...",
            "  ✓ Dead-letter queue test...",
            "  PASSED (89ms)",
            "",
            "Test Suite 4/6: Analytics Engine",
            "  ✓ Recording metrics...",
            "  ✓ Alert rule evaluation...",
            "  ✓ Cost tracking...",
            "  ✓ Dashboard generation...",
            "  PASSED (456ms)",
            "",
            "Test Suite 5/6: Learning Engine",
            "  ✓ Pattern detection...",
            "  ✓ Confidence scoring...",
            "  ✓ Proposal workflow...",
            "  ✓ Governor review flow...",
            "  PASSED (782ms)",
            "",
            "Test Suite 6/6: Cross-Component Integration",
            "  ✓ Full task flow...",
            "  ✓ Closed loop test...",
            "  PASSED (2.1s)",
            "",
            "============================",
            "Total: 6/6 tests passed ✓",
            "All Phase 2 services operational",
            "",
            "🏆 PHASE 2 VALIDATION COMPLETE",
          ]}
          startFrame={150}
          perLineDelay={12}
        />
      </TerminalWindow>
    </>
  );
};

// Sequence 9: Closing / CTA
export const Closing: React.FC = () => {
  return (
    <>
      <div
        style={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          textAlign: "center",
        }}
      >
        <h1
          style={{
            fontSize: "64px",
            fontWeight: "600",
            color: "#00d4aa",
            marginBottom: "24px",
          }}
        >
          VJSOS-AI Phase 2
        </h1>
        <div
          style={{
            display: "flex",
            gap: "24px",
            justifyContent: "center",
            marginBottom: "40px",
          }}
        >
          {["Skill Registry", "Plugin Manager", "Message Bus", "Analytics", "Learning"].map(
            (item) => (
              <div
                key={item}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  fontSize: "20px",
                }}
              >
                <span style={{ color: "#98c379", fontSize: "28px" }}>✓</span>
                <span style={{ color: "#e06c75" }}>{item}</span>
              </div>
            )
          )}
        </div>
        <div style={{ fontSize: "20px", color: "#abb2bf", maxWidth: "700px" }}>
          Production Ready • Five services integrated • One message bus • Constitutional governance
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          bottom: "80px",
          left: "50%",
          transform: "translateX(-50%)",
          fontSize: "18px",
          color: "#98c379",
        }}
      >
        github.com/your-org/vjsos-ai • docs.vjsos-ai.dev • discord.gg/vjsos-ai
      </div>
      <div
        style={{
          position: "absolute",
          bottom: "30px",
          left: "50%",
          transform: "translateX(-50%)",
          fontSize: "14px",
          color: "#5c6370",
        }}
      >
        #VJSOS #AIAgents #PlatformEngineering #Python #OpenSource
      </div>
    </>
  );
};

// Reusable Components

export const TerminalWindow: React.FC<{
  title: string;
  width?: number;
  height?: number;
  left?: number;
  top?: number;
  startFrame?: number;
  duration?: number;
  children?: React.ReactNode;
}> = ({ title, width = 640, height = 360, left, top, startFrame = 0, duration, children }) => {
  const frame = useCurrentFrame();
  const cfg = useVideoConfig();
  const { width: vw } = cfg;
  const actualWidth = width || vw * 0.7;
  const actualLeft = left ?? (vw - actualWidth) / 2;

  const opacity = startFrame > 0
    ? interpolate(frame, [startFrame, startFrame + 30], [0, 1])
    : 1;

  return (
    <div
      style={{
        position: "absolute",
        left: actualLeft,
        top: top,
        width: actualWidth,
        height: height,
        backgroundColor: "#2d2d44",
        borderRadius: "8px",
        border: "1px solid #383858",
        boxShadow: "0 10px 60px rgba(0, 0, 0, 0.5)",
        opacity,
      }}
    >
      {/* Terminal title bar */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "8px",
          padding: "8px 12px",
          backgroundColor: "#252535",
          borderTopLeftRadius: "8px",
          borderTopRightRadius: "8px",
          borderBottom: "1px solid #383858",
        }}
      >
        <div style={{ display: "flex", gap: "6px" }}>
          <div style={{ width: "12px", height: "12px", borderRadius: "50%", backgroundColor: "#e06c75" }} />
          <div style={{ width: "12px", height: "12px", borderRadius: "50%", backgroundColor: "#e5c07b" }} />
          <div style={{ width: "12px", height: "12px", borderRadius: "50%", backgroundColor: "#98c379" }} />
        </div>
        <span style={{ fontSize: "12px", color: "#7a7a9e", fontFamily: "monospace" }}>
          {title}
        </span>
      </div>
      <div
        style={{
          height: `calc(100% - 32px)`,
          padding: "12px",
          overflow: "hidden",
          fontFamily: "monospace",
          fontSize: "14px",
          lineHeight: "1.4",
        }}
      >
        {children}
      </div>
    </div>
  );
};

export const TerminalLine: React.FC<{
  text: string;
  delayFrames?: number;
}> = ({ text, delayFrames = 0 }) => {
  const frame = useCurrentFrame();
  if (frame < delayFrames) return null;

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        marginBottom: "4px",
      }}
    >
      <span style={{ color: "#61afef", marginRight: "8px" }}>$</span>
      <span style={{ color: "#d4d4d4", fontFamily: "monospace" }}>{text}</span>
    </div>
  );
};

export const TerminalOutput: React.FC<{
  lines: string[];
  startFrame?: number;
  perLineDelay?: number;
}> = ({ lines, startFrame = 0, perLineDelay = 30 }) => {
  const frame = useCurrentFrame();

  const shown = lines.map((line, i) => {
    const lineFrame = startFrame + i * perLineDelay;
    if (frame >= lineFrame) {
      return (
        <div
          key={i}
          style={{
            color: getLineColor(line),
            fontFamily: "monospace",
            marginBottom: "2px",
          }}
        >
          {line}
        </div>
      );
    }
    return null;
  });

  // Typing animation effect
  const lastShownIdx = lines.findIndex((_, i) => frame < startFrame + i * perLineDelay);
  const showCursor = lastShownIdx > 0 && frame < startFrame + lines.length * perLineDelay + 10;

  return (
    <>
      {shown}
      {showCursor && (
        <span
          style={{
            opacity: (frame % 30) / 30 > 0.5 ? 1 : 0,
            color: "#d4d4d4",
            fontFamily: "monospace",
          }}
        >
          ▋
        </span>
      )}
    </>
  );
};

function getLineColor(line: string): string {
  if (line.includes("✓") || line.includes("PASSED")) return "#98c379";
  if (line.includes("✗") || line.includes("FAILED")) return "#e06c75";
  if (line.startsWith("$")) return "#61afef";
  if (line.includes("Test Suite") || line.includes("Total:")) return "#c678dd";
  if (line.includes("Phase") || line.includes("COMPLETE")) return "#e5c07b";
  if (line.startsWith("  ")) return "#d4d4d4";
  return "#d4d4d4";
}

export const SectionTitle: React.FC<{
  title: string;
  startFrame: number;
  duration: number;
}> = ({ title, startFrame, duration }) => {
  const frame = useCurrentFrame();
  const progress = Math.max(0, Math.min(1, (frame - startFrame) / duration));

  if (frame < startFrame) return null;
  if (frame > startFrame + duration) return null;

  return (
    <div
      style={{
        position: "absolute",
        top: "60px",
        left: "50%",
        transform: "translateX(-50%)",
        textAlign: "center",
        opacity: progress,
      }}
    >
      <h2
        style={{
          fontSize: "36px",
          fontWeight: "600",
          color: "#ffffff",
          marginBottom: "8px",
          letterSpacing: "2px",
        }}
      >
        {title}
      </h2>
      <div
        style={{
          width: "400px",
          height: "2px",
          backgroundColor: "#00d4aa",
          margin: "0 auto",
        }}
      />
    </div>
  );
};

export const TitleCard: React.FC<{
  title: string;
  subtitle: string;
  startFrame: number;
  duration: number;
}> = ({ title, subtitle, startFrame, duration }) => {
  const frame = useCurrentFrame();
  if (frame < startFrame) return null;

  const progress = Math.min(1, (frame - startFrame) / 60);
  const opacity = progress;

  return (
    <div
      style={{
        position: "absolute",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        textAlign: "center",
        opacity,
      }}
    >
      <h1
        style={{
          fontSize: "72px",
          fontWeight: "700",
          color: "#00d4aa",
          marginBottom: "16px",
          letterSpacing: "4px",
        }}
      >
        {title}
      </h1>
      <h2
        style={{
          fontSize: "32px",
          fontWeight: "400",
          color: "#d4d4d4",
        }}
      >
        {subtitle}
      </h2>
    </div>
  );
};

export const ArchitectureDiagram: React.FC<{
  startFrame: number;
  duration: number;
}> = ({ startFrame, duration }) => {
  const frame = useCurrentFrame();
  if (frame < startFrame) return null;

  const nodes = [
    { name: "Skill Registry", x: 100, y: 300, color: "#00d4aa" },
    { name: "Plugin Manager", x: 100, y: 450, color: "#00d4aa" },
    { name: "Message Bus", x: 400, y: 375, color: "#00d4aa" },
    { name: "Analytics Engine", x: 700, y: 300, color: "#00d4aa" },
    { name: "Learning Engine", x: 700, y: 450, color: "#00d4aa" },
  ];

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        marginTop: "100px",
      }}
    >
      <div style={{ position: "relative", width: "800px", height: "500px" }}>
        {/* Background grid */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            backgroundImage: `
              linear-gradient(rgba(45, 45, 61, 0.2) 1px, transparent 1px),
              linear-gradient(90deg, rgba(45, 45, 61, 0.2) 1px, transparent 1px)
            `,
            backgroundSize: "40px 40px",
          }}
        />
        {/* Connecting lines */}
        <svg
          style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
        >
          {nodes.map((a, i) =>
            nodes.slice(i + 1).map((b, j) => (
              <line
                key={`${i}-${j}`}
                x1={a.x + 100}
                y1={a.y + 25}
                x2={b.x + 100}
                y2={b.y + 25}
                stroke="#00d4aa"
                strokeWidth={1}
                opacity={0.4}
                strokeDasharray="4 4"
              />
            ))
          )}
        </svg>
        {/* Nodes */}
        {nodes.map((node) => (
          <div
            key={node.name}
            style={{
              position: "absolute",
              left: node.x,
              top: node.y,
              width: "200px",
              padding: "16px",
              backgroundColor: "#2d2d44",
              borderRadius: "8px",
              border: `2px solid ${node.color}`,
              boxShadow: `0 0 20px ${node.color}40`,
            }}
          >
            <div style={{ fontSize: "14px", fontWeight: "600", color: "#fff" }}>
              {node.name}
            </div>
            <div style={{ fontSize: "11px", color: "#7a7a9e", marginTop: "4px" }}>
              Click to expand
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export const JsonCallout: React.FC<{
  data: Record<string, unknown>;
  startFrame: number;
  duration: number;
  position: { top?: number; right?: number; left?: number; bottom?: number };
}> = ({ data, startFrame, duration, position }) => {
  const frame = useCurrentFrame();
  const cfg = useVideoConfig();
  const { width } = cfg;

  const actualLeft = position.left ?? position.right
    ? position.right
      ? width - position.right - 300
      : position.left
    : width / 2 - 150;

  if (frame < startFrame) return null;
  const elapsed = frame - startFrame;
  const opacity = elapsed < 30 ? elapsed / 30 : 1;

  return (
    <div
      style={{
        position: "absolute",
        ...position,
        left: actualLeft,
        top: position.top ?? 200,
        width: "280px",
        backgroundColor: "rgba(26, 26, 36, 0.95)",
        backdropFilter: "blur(8px)",
        borderRadius: "8px",
        border: "1px solid #383858",
        padding: "12px",
        fontSize: "13px",
        fontFamily: "monospace",
        opacity,
        boxShadow: "0 10px 40px rgba(0, 0, 0, 0.4)",
      }}
    >
      <div style={{ color: "#00d4aa", marginBottom: "8px", fontWeight: "600" }}>
        📋 skill.json
      </div>
      {Object.entries(data).map(([key, value]) => (
        <div
          key={key}
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: "4px",
          }}
        >
          <span style={{ color: "#d4d4d4" }}>{key}:</span>
          <span style={{ color: "#98c379" }}>{typeof value === "string" ? `"${value}"` : String(value)}</span>
        </div>
      ))}
    </div>
  );
};

export const DashboardMetrics: React.FC<{
  startFrame: number;
  duration: number;
}> = ({ startFrame, duration }) => {
  const frame = useCurrentFrame();
  if (frame < startFrame) return null;

  return (
    <div
      style={{
        position: "absolute",
        bottom: "120px",
        left: "50%",
        transform: "translateX(-50%)",
        display: "flex",
        gap: "24px",
      }}
    >
      {[
        { label: "Tasks", value: "142", color: "#61afef" },
        { label: "Success", value: "98.2%", color: "#98c379" },
        { label: "Latency", value: "4.2s", color: "#00d4aa" },
        { label: "Cost", value: "$15.55", color: "#e5c07b" },
      ].map((metric) => (
        <div
          key={metric.label}
          style={{
            textAlign: "center",
            padding: "12px 24px",
            backgroundColor: "rgba(26, 26, 36, 0.9)",
            borderRadius: "8px",
            border: "1px solid #383858",
          }}
        >
          <div style={{ fontSize: "24px", fontWeight: "700", color: metric.color }}>
            {metric.value}
          </div>
          <div style={{ fontSize: "12px", color: "#7a7a9e" }}>{metric.label}</div>
        </div>
      ))}
    </div>
  );
};

export const TealAccentLine: React.FC<{
  x1: number;
  x2: number;
  y: number;
  startFrame: number;
  duration: number;
}> = ({ x1, x2, y, startFrame, duration }) => {
  const frame = useCurrentFrame();
  if (frame < startFrame) return null;

  return (
    <svg
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        pointerEvents: "none",
      }}
    >
      <line
        x1={x1}
        y1={y}
        x2={x2}
        y2={y}
        stroke="#00d4aa"
        strokeWidth={2}
        opacity="0.6"
      />
    </svg>
  );
};