import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
 base: "/",
 plugins: [react()],
 preview: {
  port: 8001,
  strictPort: true,
 },
 server: {
  port: 8001,
  strictPort: true,
  host: true,
  origin: "http://0.0.0.0:8080",
 },
});