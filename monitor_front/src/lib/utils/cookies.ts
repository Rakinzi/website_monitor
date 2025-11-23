const isBrowser = typeof document !== 'undefined';

export function setCookie(name: string, value: string, days = 7) {
  if (!isBrowser) return;
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  const secure = window.location.protocol === 'https:' ? '; Secure' : '';
  document.cookie = `${name}=${encodeURIComponent(value)}; Expires=${expires}; Path=/; SameSite=Strict${secure}`;
}

export function getCookie(name: string): string | null {
  if (!isBrowser) return null;
  const cookies = document.cookie ? document.cookie.split('; ') : [];
  for (const cookie of cookies) {
    const [key, ...vals] = cookie.split('=');
    if (key === name) {
      return decodeURIComponent(vals.join('='));
    }
  }
  return null;
}

export function deleteCookie(name: string) {
  if (!isBrowser) return;
  document.cookie = `${name}=; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Path=/; SameSite=Strict`;
}
