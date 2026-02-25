"use client";
import { useEffect } from "react";

export function ViewTracker({ articleId, title }: { articleId: string; title: string }) {
  useEffect(() => {
    fetch("/api/views", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ articleId, title }),
    });
  }, [articleId]);

  return null;
}
