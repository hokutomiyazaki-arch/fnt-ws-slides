/* kiosk.js — 会員向けの公開ページを「持ち出しにくく」する共通スクリプト
 *
 * 🔴 これは鍵ではない。速度バンプ（面倒にするだけ）。
 *    URLを一度でも知った人は、履歴・ブックマーク・共有シートから開ける。
 *    本当に締め出すなら URL を変えるしかない（README の「効かないこと」を読む）。
 *
 * やること
 *   1. Android/Chrome の「ホーム画面に追加」バナーを出さない
 *   2. 長押しメニュー・テキスト選択・ドラッグを止める（URLとリンクを取りにくくする）
 *   3. 最初のタップで全画面にする（アドレスバーが隠れる＝URLが見えなくなる）
 *   4. 全画面を抜けたら、次のタップでまた全画面にする
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
  // 入力欄の中だけは普通に使えるようにする（検索窓を壊さないため）
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
    'img,a{-webkit-user-drag:none}';
  (document.head || root).appendChild(css);

  // ── 3. 最初のタップで全画面 ──────────────────────────────
  // 全画面化はユーザー操作の中でしか呼べない（ブラウザの決まり）ので、
  // 読み込み直後ではなく「最初に触ったとき」に入れる。
  var req = root.requestFullscreen || root.webkitRequestFullscreen ||
            root.mozRequestFullScreen || root.msRequestFullscreen;

  function isFull() {
    return !!(document.fullscreenElement || document.webkitFullscreenElement);
  }

  function enter() {
    if (!req || isFull()) return;
    try {
      var p = req.call(root, { navigationUI: 'hide' });
      if (p && p.catch) p.catch(function () {});   // 断られても何もしない
    } catch (e) { /* 対応していない端末はここに来る。放っておく */ }
  }

  // 4. 抜けたらまた入れるよう、毎回のタップで試す（既に全画面なら何もしない）
  ['pointerdown', 'touchend', 'click'].forEach(function (type) {
    document.addEventListener(type, enter, { capture: true, passive: true });
  });

  // 全画面に対応していない端末（iPhoneのSafariなど）でも、
  // 少しでもアドレスバーを縮めるため、読み込み後にわずかにスクロールする。
  window.addEventListener('load', function () {
    if (req) return;
    setTimeout(function () { window.scrollTo(0, 1); }, 120);
  });
})();
