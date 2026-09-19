/* kiosk.js — 会員向けの公開ページを「持ち出しにくく」する共通スクリプト
 *
 * 🔴 これは鍵ではない。速度バンプ（面倒にするだけ）。
 *    URLを一度でも知った人は、履歴・ブックマーク・共有シートから開ける。
 *    本当に締め出すのは年1回のアドレス付け替え（shared/rotate_url.py）。
 *
 * やること
 *   1. Android/Chrome の「ホーム画面に追加」バナーを出さない
 *   2. 長押しメニュー・テキスト選択・ドラッグを止める（URLとリンクを取りにくくする）
 *   3. 右下に「全画面」ボタンを出す ← v2 で追加
 *   4. 最初のタップでも全画面を試す（黙って失敗しても①のボタンが残る）
 *
 * 🔴 v2（2026-09-19）で見えるボタンを足した理由
 *    v1 は「最初のタップで全画面」だけだった。全画面は端末やブラウザの設定で
 *    断られることがあり、断られても画面に何も出ないので、
 *    使う側も直す側も「効いていない」としか分からなかった。
 *    ボタンなら、押して変わらなければ「この端末では無理」と切り分けられる。
 *
 * 置き方：ページの <head> に
 *   <script src="kiosk.js" defer></script>        （階層が下なら ../kiosk.js）
 * 正本：fnt-neuro-community/shared/kiosk.js
 */
(function () {
  'use strict';

  var root = document.documentElement;

  // ── 1. インストールを促さない ────────────────────────────
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
  });

  // ── 2. 長押し・選択・ドラッグを止める ────────────────────
  function inField(t) {
    return t && t.closest && t.closest('input, textarea, [contenteditable]');
  }
  ['contextmenu', 'dragstart', 'selectstart'].forEach(function (type) {
    document.addEventListener(type, function (e) {
      if (!inField(e.target)) e.preventDefault();
    }, { capture: true });
  });

  var css = document.createElement('style');
  css.textContent =
    'html{-webkit-touch-callout:none}' +
    'body{-webkit-user-select:none;user-select:none}' +
    'input,textarea,[contenteditable]{-webkit-user-select:text;user-select:text}' +
    'img,a{-webkit-user-drag:none}' +
    '#kioskFs{position:fixed;z-index:2147483647;' +
      'right:calc(12px + env(safe-area-inset-right,0px));' +
      'bottom:calc(12px + env(safe-area-inset-bottom,0px));' +
      'width:44px;height:44px;border-radius:50%;border:1px solid rgba(0,0,0,.18);' +
      'background:rgba(255,255,255,.88);color:#333;font-size:17px;line-height:1;' +
      'display:grid;place-items:center;cursor:pointer;padding:0;' +
      '-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);' +
      'box-shadow:0 1px 6px rgba(0,0,0,.18)}' +
    '#kioskFs:active{transform:scale(.94)}' +
    '@media print{#kioskFs{display:none}}';
  (document.head || root).appendChild(css);

  // ── 3/4. 全画面 ──────────────────────────────────────────
  var req = root.requestFullscreen || root.webkitRequestFullscreen ||
            root.mozRequestFullScreen || root.msRequestFullscreen;
  var exit = document.exitFullscreen || document.webkitExitFullscreen ||
             document.mozCancelFullScreen || document.msExitFullscreen;

  function isFull() {
    return !!(document.fullscreenElement || document.webkitFullscreenElement ||
              document.mozFullScreenElement || document.msFullscreenElement);
  }

  function enter() {
    if (!req || isFull()) return;
    try {
      var p = req.call(root, { navigationUI: 'hide' });
      if (p && p.catch) p.catch(function () {});   // 断られても黙って戻る
    } catch (e) { /* 対応していない端末 */ }
  }

  // この端末で全画面が使えないなら、ボタンは出さない（押しても何も起きないボタンは邪魔）
  if (!req || document.fullscreenEnabled === false) return;

  var btn = document.createElement('button');
  btn.id = 'kioskFs';
  btn.type = 'button';
  btn.setAttribute('aria-label', '全画面');
  btn.textContent = '⛶';

  btn.addEventListener('click', function (e) {
    e.stopPropagation();
    if (isFull()) {
      if (exit) exit.call(document);
    } else {
      enter();
    }
  });

  function sync() {
    var full = isFull();
    btn.textContent = full ? '✕' : '⛶';
    btn.setAttribute('aria-label', full ? '全画面をやめる' : '全画面');
  }
  ['fullscreenchange', 'webkitfullscreenchange'].forEach(function (t) {
    document.addEventListener(t, sync);
  });

  function mount() {
    (document.body || root).appendChild(btn);
    sync();
  }
  if (document.body) mount();
  else document.addEventListener('DOMContentLoaded', mount);

  // 最初のタップでも試す（ボタンを押さなくても全画面になる端末のため）
  var once = function (e) {
    if (e.target !== btn) enter();
    document.removeEventListener('pointerdown', once, true);
    document.removeEventListener('touchend', once, true);
    document.removeEventListener('click', once, true);
  };
  ['pointerdown', 'touchend', 'click'].forEach(function (t) {
    document.addEventListener(t, once, { capture: true, passive: true });
  });
})();
