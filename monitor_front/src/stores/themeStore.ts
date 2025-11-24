import { writable } from 'svelte/store';

export type Theme = 'light' | 'dark';

function createThemeStore() {
  const getInitialTheme = (): Theme => {
    if (typeof window === 'undefined') return 'dark';

    const stored = localStorage.getItem('theme');
    if (stored === 'light' || stored === 'dark') {
      return stored;
    }

    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }

    return 'light';
  };

  const applyTheme = (theme: Theme) => {
    if (typeof window === 'undefined') return;

    const html = document.documentElement;

    if (theme === 'dark') {
      html.classList.add('dark');
      html.classList.remove('light');
    } else {
      html.classList.add('light');
      html.classList.remove('dark');
    }

    localStorage.setItem('theme', theme);
  };

  const { subscribe, set, update } = writable<Theme>(getInitialTheme());

  return {
    subscribe,
    toggle: () => {
      update(theme => {
        const newTheme = theme === 'light' ? 'dark' : 'light';
        applyTheme(newTheme);
        return newTheme;
      });
    },
    set: (theme: Theme) => {
      applyTheme(theme);
      set(theme);
    },
    init: () => {
      const theme = getInitialTheme();
      applyTheme(theme);
      set(theme);
    }
  };
}

export const themeStore = createThemeStore();
