/**
 * Visual RAGForge assistant avatar.
 *
 * Pure UI layer over the existing chat state — three states, no network:
 *   idle     → static face with a very subtle floating/breathing motion
 *   thinking → waiting on the backend; antenna pulse + gentle head sway
 *   speaking → assistant response is being presented; mouth animates
 *              in an organic rhythm with an occasional blink
 *
 * Animations run through GSAP timelines created per state and killed
 * on state change / unmount. A gsap.matchMedia guard means nothing
 * animates when the user prefers reduced motion.
 */
import { useEffect, useRef } from "react";
import gsap from "gsap";

const SIZE_CLASS = {
  sm: "h-7 w-7", // matches existing message avatars
  md: "h-8 w-8",
};

export function BotAvatar({ state = "idle", size = "sm", className = "" }) {
  const svgRef = useRef(null);

  useEffect(() => {
    const svg = svgRef.current;
    if (!svg) return;

    const head = svg.querySelector(".bot-head");
    const antenna = svg.querySelector(".bot-antenna");
    const eyes = svg.querySelector(".bot-eyes");
    const mouth = svg.querySelector(".bot-mouth");

    const mm = gsap.matchMedia();

    mm.add("(prefers-reduced-motion: no-preference)", () => {
      const timelines = [];
      const add = (tl) => {
        timelines.push(tl);
        return tl;
      };

      // Shared blink so the face feels alive but not busy.
      const addBlink = (repeatDelay) =>
        add(
          gsap.timeline({ repeat: -1, repeatDelay })
            .to(eyes, { scaleY: 0.15, transformOrigin: "50% 50%", duration: 0.08 })
            .to(eyes, { scaleY: 1, duration: 0.08 })
        );

      if (state === "speaking") {
        // Organic mouth rhythm — a few different heights so it never
        // looks like a mechanical open/close loop.
        add(
          gsap
            .timeline({ repeat: -1 })
            .to(mouth, { scaleY: 1, transformOrigin: "50% 50%", duration: 0.12, ease: "sine.inOut" })
            .to(mouth, { scaleY: 0.3, duration: 0.18, ease: "sine.inOut" })
            .to(mouth, { scaleY: 0.85, duration: 0.1, ease: "sine.inOut" })
            .to(mouth, { scaleY: 0.45, duration: 0.22, ease: "sine.inOut" })
            .to(mouth, { scaleY: 1, duration: 0.14, ease: "sine.inOut" })
            .to(mouth, { scaleY: 0.25, duration: 0.16, ease: "sine.inOut" })
        );
        // Subtle head bob while talking.
        add(
          gsap
            .timeline({ repeat: -1 })
            .to(head, { y: -0.3, duration: 0.35, ease: "sine.inOut" })
            .to(head, { y: 0.3, duration: 0.35, ease: "sine.inOut" })
            .to(head, { y: 0, duration: 0.35, ease: "sine.inOut" })
        );
        addBlink(3.2);
      } else if (state === "thinking") {
        // Antenna pulses, head sways gently — clearly "processing".
        add(
          gsap
            .timeline({ repeat: -1 })
            .to(antenna, { scale: 1.35, transformOrigin: "50% 100%", duration: 0.35, ease: "sine.inOut" })
            .to(antenna, { scale: 1, duration: 0.35, ease: "sine.inOut" })
        );
        add(
          gsap
            .timeline({ repeat: -1, repeatDelay: 0.2 })
            .to(head, { rotation: 4, transformOrigin: "50% 85%", duration: 0.4, ease: "sine.inOut" })
            .to(head, { rotation: -4, duration: 0.4, ease: "sine.inOut" })
            .to(head, { rotation: 0, duration: 0.4, ease: "sine.inOut" })
        );
        addBlink(2.4);
      } else {
        // Idle: one barely-there float + slow antenna dimming.
        add(
          gsap
            .timeline({ repeat: -1 })
            .to(head, { y: -0.25, duration: 1.6, ease: "sine.inOut" })
            .to(head, { y: 0.25, duration: 1.6, ease: "sine.inOut" })
        );
        add(
          gsap
            .timeline({ repeat: -1, repeatDelay: 1.2 })
            .to(antenna, { opacity: 0.55, duration: 0.9, ease: "sine.inOut" })
            .to(antenna, { opacity: 1, duration: 0.9, ease: "sine.inOut" })
        );
      }

      return () => {
        timelines.forEach((tl) => tl.kill());
        gsap.set([head, antenna, eyes, mouth], { clearProps: "all" });
      };
    });

    return () => mm.revert();
  }, [state]);

  const isSpeaking = state === "speaking";

  return (
    <div
      className={`flex shrink-0 items-center justify-center rounded-full bg-purple-bg ${
        SIZE_CLASS[size] || SIZE_CLASS.sm
      } ${className}`}
      role="img"
      aria-label={
        state === "thinking"
          ? "RAGForge thinking"
          : isSpeaking
            ? "RAGForge responding"
            : "RAGForge"
      }
    >
      <svg ref={svgRef} width="18" height="18" viewBox="0 0 18 18" aria-hidden="true">
        {/* Antenna */}
        <line x1="9" y1="2" x2="9" y2="3.8" stroke="#7C5CFF" strokeWidth="1" />
        <circle className="bot-antenna" cx="9" cy="1.6" r="0.9" fill="#7C5CFF" />
        {/* Head */}
        <g className="bot-head">
          <rect x="3" y="3.8" width="12" height="10" rx="3" fill="none" stroke="#7C5CFF" strokeWidth="1.2" />
          {/* Eyes */}
          <g className="bot-eyes">
            <circle cx="6.5" cy="7.6" r="1.1" fill="#7C5CFF" />
            <circle cx="11.5" cy="7.6" r="1.1" fill="#7C5CFF" />
          </g>
          {/* Mouth — thin line when quiet, openable box while speaking */}
          {isSpeaking ? (
            <rect className="bot-mouth" x="6" y="9.7" width="6" height="2.8" rx="1.4" fill="#7C5CFF" />
          ) : (
            <rect className="bot-mouth" x="6" y="10.6" width="6" height="1.2" rx="0.6" fill="#7C5CFF" />
          )}
        </g>
      </svg>
    </div>
  );
}
