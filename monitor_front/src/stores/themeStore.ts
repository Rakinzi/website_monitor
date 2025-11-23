import { writable } from 'svelte/store';

export type Theme = 'light' | 'dark';

function createThemeStore() {
  // Check localStorage or system preference
  const getInitialTheme = (): Theme => {
    if (typeof window === 'undefined') return 'dark';

    const stored = localStorage.getItem('theme');
    if (stored === 'light' || stored === 'dark') {
      return stored;
    }

    // Check system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }

    return 'light';
  };

  const { subscribe, set, update } = writable<Theme>(getInitialTheme());

  return {
    subscribe,
    toggle: () => {
      update(theme => {
        const newTheme = theme === 'light' ? 'dark' : 'light';
        if (typeof window !== 'undefined') {
          localStorage.setItem('theme', newTheme);
          document.documentElement.classList.remove('light', 'dark');
          document.documentElement.classList.add(newTheme);
        }
        return newTheme;
      });
    },
    set: (theme: Theme) => {
      if (typeof window !== 'undefined') {
        localStorage.setItem('theme', theme);
        document.documentElement.classList.remove('light', 'dark');
        document.documentElement.classList.add(theme);
      }
      set(theme);
    },
    init: () => {
      const theme = getInitialTheme();
      if (typeof window !== 'undefined') {
        document.documentElement.classList.add(theme);
      }
      set(theme);
    }
  };
}

export const themeStore = createThemeStore();
