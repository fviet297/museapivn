/* Muse2API Cookie 导入 —— 读取 muse.ai 的 cookie 并 POST 到 muse2api 服务。
 *
 * 关键点：用 chrome.cookies 而不是 document.cookie。
 * muse.ai 的 4 条核心 cookie（hatch_sess / hatch_gw / hatch_vml /
 * hatch_native_auth_device）都带 httpOnly，网页 JS 读不到，
 * 只有浏览器扩展的 cookies 接口能拿到。
 */

const $ = (id) => document.getElementById(id);
const STORE = 'muse2api_ext_cfg';

// 与后端 engine.ESSENTIAL_COOKIES 保持一致：hatch_gw 为网关路由缓存，非必需
const ESSENTIAL = ['hatch_sess', 'hatch_vml', 'hatch_native_auth_device'];

function log(html, cls) {
  const el = $('log');
  el.className = 'show';
  el.innerHTML = cls ? `<span class="${cls}">${html}</span>` : html;
}

/* 规范化服务地址：去掉结尾斜杠和 /v1 后缀 */
function normBase(v) {
  let s = (v || '').trim();
  if (!s) return '';
  if (!/^https?:\/\//i.test(s)) s = 'https://' + s;
  s = s.replace(/\/+$/, '');
  s = s.replace(/\/v1$/i, '');
  return s;
}

async function loadCfg() {
  const o = await chrome.storage.local.get(STORE);
  const c = o[STORE] || {};
  if (c.base) $('base').value = c.base;
  if (c.key) $('key').value = c.key;
  if (c.label) $('label').value = c.label;
  // 没有配置过就尝试从当前标签页猜一个（用户在管理页上时）
  if (!c.base) {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      const u = tab && tab.url ? new URL(tab.url) : null;
      if (u && /\/admin/.test(u.pathname)) {
        $('base').value = u.origin;
        const k = new URLSearchParams(u.search).get('key');
        if (k) $('key').value = k;
      }
    } catch (e) { /* 忽略 */ }
  }
}

async function saveCfg() {
  await chrome.storage.local.set({
    [STORE]: {
      base: normBase($('base').value),
      key: $('key').value.trim(),
      label: $('label').value.trim(),
    },
  });
}

async function grabCookies() {
  const all = await chrome.cookies.getAll({ domain: 'muse.ai' });
  const out = {}, exp = {};
  for (const c of all) {
    const dom = (c.domain || '').replace(/^\./, '');
    if (!dom.endsWith('muse.ai')) continue;
    out[c.name] = c.value;
    if (c.expirationDate) exp[c.name] = Math.floor(c.expirationDate);
  }
  return { cookies: out, expires: exp };
}

async function run() {
  const base = normBase($('base').value);
  const key = $('key').value.trim();
  const label = $('label').value.trim();

  if (!base) return log('Vui lòng điền địa chỉ dịch vụ trước', 'bad');
  if (!key) return log('Vui lòng điền API Key trước', 'bad');

  $('go').disabled = true;
  log('Đang đọc Cookie muse.ai…');

  try {
    const { cookies, expires } = await grabCookies();
    const names = Object.keys(cookies);
    if (!names.length) {
      return log('Không đọc được Cookie muse.ai.\nHãy mở và đăng nhập '
                 + 'https://muse.ai/ trong trình duyệt này, rồi quay lại nhấn lần nữa.', 'bad');
    }
    const missing = ESSENTIAL.filter((n) => !(n in cookies));
    if (missing.length) {
      log(`Đọc được ${names.length} Cookie nhưng thiếu mục cốt lõi: ${missing.join(', ')}\n`
          + 'Nghĩa là trình duyệt này chưa đăng nhập thành công. Hãy đăng nhập đến khi thấy giao diện chat rồi thử lại.', 'warn');
      return;
    }

    log(`Đọc được ${names.length} Cookie, đang tải lên ${base} …`);

    const r = await fetch(base + '/admin/accounts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key,
      },
      body: JSON.stringify({ label, cookies, expires }),
    });

    const text = await r.text();
    let data;
    try { data = JSON.parse(text); } catch (e) { data = { raw: text }; }

    if (r.status === 401) {
      return log('API Key không đúng (dịch vụ trả về 401).\n'
                 + 'Hãy sao chép API Key đúng ở đầu tab "Bể tài khoản" trong trang quản trị.', 'bad');
    }
    if (!r.ok) {
      return log(`Nhập thất bại: HTTP ${r.status}\n${text.slice(0, 300)}`, 'bad');
    }

    const a = (data.added && data.added[0]) || {};
    await saveCfg();
    log(`✓ Nhập thành công\nNhãn tài khoản: ${a.label || label || '(tự động)'}\n`
        + `ID tài khoản: ${a.id || '?'}\nSố Cookie: ${a.cookie_count || names.length}\n`
        + `Có hiệu lực đến: ${a.expires_at ? new Date(a.expires_at * 1000).toLocaleString() : 'không rõ'}\n`
        + (data.warning ? `\nLưu ý: ${data.warning}` : ''), 'ok');
  } catch (e) {
    log('Đã xảy ra lỗi: ' + (e && e.message ? e.message : String(e))
        + '\n\nNguyên nhân thường gặp:\n'
        + '· Địa chỉ dịch vụ sai hoặc dịch vụ chưa khởi động\n'
        + '· Địa chỉ này không phải https (hoặc chứng chỉ không được tin cậy)\n'
        + '· Trình duyệt chặn yêu cầu cross-origin', 'bad');
  } finally {
    $('go').disabled = false;
  }
}

$('go').addEventListener('click', run);
loadCfg();
