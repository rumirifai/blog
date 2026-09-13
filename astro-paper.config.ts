import { defineAstroPaperConfig } from "./src/types/config";

export default defineAstroPaperConfig({
  site: {
    url: "https://rumirifai.blogspot.com/",
    title: "Tulisan Rumi",
    description: "Tulisan yang isinya pengalaman, pemikiran, serta keresahan yang gua rasakan.",
    author: "Rumi Rifai",
    profile: "https://www.blogger.com/profile/10038969407574556552",
    ogImage: "default-og.jpg",
    lang: "id",
    timezone: "Asia/Jakarta",
    dir: "ltr",
  },
  posts: {
    perPage: 4,
    perIndex: 4,
    scheduledPostMargin: 15 * 60 * 1000,
  },
  features: {
    lightAndDarkMode: true,
    dynamicOgImage: true,
    showArchives: true,
    showBackButton: true,
    editPost: {
      enabled: false,
    },
    search: "pagefind",
  },
  socials: [
    { name: "x", url: "https://x.com/your-handle" },
    { name: "mail", url: "mailto:your-email@example.com" },
  ],
  shareLinks: [
    { name: "whatsapp", url: "https://wa.me/?text=" },
    { name: "facebook", url: "https://www.facebook.com/sharer.php?u=" },
    { name: "x",        url: "https://x.com/intent/post?url=" },
    { name: "telegram", url: "https://t.me/share/url?url=" },
    { name: "pinterest", url: "https://pinterest.com/pin/create/button/?url=" },
    { name: "mail",     url: "mailto:?subject=See%20this%20post&body=" },
  ],
});