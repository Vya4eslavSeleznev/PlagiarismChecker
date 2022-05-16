function getCsrfTokenValue() {
  const cookie = document.cookie;

  if (!cookie) return null;

  const cookies = cookie.split(';');
  const regExp = new RegExp(/(csrf_access_token=)(.+)/, 'g');
  const csrfCookie = cookies.find((x) => regExp.test(x));

  if (!csrfCookie) return null;

  return csrfCookie.replace(regExp, '$2');
}