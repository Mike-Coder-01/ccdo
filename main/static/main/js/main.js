const body = document.body;
const header = document.querySelector('.site-header');
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');
const backTop = document.querySelector('.back-top');

window.addEventListener('load', () => setTimeout(() => document.querySelector('.page-loader')?.classList.add('hide'), 350));
function updateHeader(){header?.classList.toggle('scrolled',window.scrollY>35);backTop?.classList.toggle('show',window.scrollY>600)}
window.addEventListener('scroll',updateHeader,{passive:true});updateHeader();
navToggle?.addEventListener('click',()=>{const open=navMenu.classList.toggle('open');navToggle.setAttribute('aria-expanded',String(open));body.classList.toggle('menu-open',open);navToggle.classList.toggle('active',open)});
navMenu?.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{navMenu.classList.remove('open');navToggle?.setAttribute('aria-expanded','false');body.classList.remove('menu-open')}));
document.querySelectorAll('a[href^="#"]').forEach(link=>link.addEventListener('click',event=>{const target=document.querySelector(link.getAttribute('href'));if(!target)return;event.preventDefault();target.scrollIntoView({behavior:'smooth',block:'start'})}));
backTop?.addEventListener('click',()=>window.scrollTo({top:0,behavior:'smooth'}));
const reducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const revealObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('in-view');revealObserver.unobserve(entry.target)}}),{threshold:.12,rootMargin:'0px 0px -40px'});
document.querySelectorAll('.reveal').forEach(el=>revealObserver.observe(el));
const slides=[...document.querySelectorAll('.beneficiary-slide')],dotsWrap=document.querySelector('.carousel-dots'),prev=document.querySelector('.carousel-btn.prev'),next=document.querySelector('.carousel-btn.next');let slideIndex=0,carouselTimer;
function renderDots(){if(!dotsWrap)return;dotsWrap.innerHTML=slides.map((_,i)=>`<button type="button" aria-label="Go to slide ${i+1}" class="${i===slideIndex?'active':''}"></button>`).join('');dotsWrap.querySelectorAll('button').forEach((dot,i)=>dot.addEventListener('click',()=>showSlide(i,true)))}
function showSlide(index,manual=false){if(!slides.length)return;slideIndex=(index+slides.length)%slides.length;slides.forEach((slide,i)=>slide.classList.toggle('active',i===slideIndex));renderDots();if(manual)restartCarousel()}
function restartCarousel(){clearInterval(carouselTimer);if(!reducedMotion)carouselTimer=setInterval(()=>showSlide(slideIndex+1),5500)}
prev?.addEventListener('click',()=>showSlide(slideIndex-1,true));next?.addEventListener('click',()=>showSlide(slideIndex+1,true));showSlide(0);restartCarousel();
const heroVisual=document.querySelector('.hero-visual');if(heroVisual&&!reducedMotion){window.addEventListener('mousemove',e=>{const x=(e.clientX/window.innerWidth-.5)*8,y=(e.clientY/window.innerHeight-.5)*5;heroVisual.style.transform=`translate(${x}px,${y}px)`},{passive:true})}
const sections=[...document.querySelectorAll('main section[id]')],navLinks=[...document.querySelectorAll('.nav-menu a[href^="#"]')];
const activeObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting)navLinks.forEach(link=>link.classList.toggle('active',link.getAttribute('href')===`#${entry.target.id}`))}),{rootMargin:'-35% 0px -55% 0px'});sections.forEach(section=>activeObserver.observe(section));

document.querySelectorAll('[data-demo-form]').forEach(form=>form.addEventListener('submit',event=>{event.preventDefault();const status=form.querySelector('.form-status');if(status){status.textContent='Thank you. This prototype form is ready to be connected to CCDO’s backend/CMS.';status.style.opacity='1'}form.reset()}));


// TYPING ANIMATION IN 
function typeWordByWordWithCursor(el, {
  charSpeed = 60,     // ms per character while typing a word
  wordPause = 300,    // pause after a word finishes, before starting the next
  holdDelay = 1500,   // pause once the whole line is fully typed
  restartDelay = 500  // pause on the blank line before retyping
} = {}) {
  if (!el) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const fullText = el.textContent.trim();
  const words = fullText.split(' ');

  const cursor = document.createElement('span');
  cursor.className = 'typing-cursor';
  cursor.textContent = '|';

  let typed = '';
  function render() {
    el.textContent = typed;
    el.appendChild(cursor);
  }

  let wordIndex = 0;
  let charIndex = 0;

  function tick() {
    const word = words[wordIndex];

    if (charIndex < word.length) {
      typed += word[charIndex];
      render();
      charIndex++;
      setTimeout(tick, charSpeed);
      return;
    }

    wordIndex++;
    charIndex = 0;

    if (wordIndex < words.length) {
      typed += ' ';
      render();
      setTimeout(tick, wordPause);
    } else {
      setTimeout(() => {
        typed = '';
        render();
        wordIndex = 0;
        charIndex = 0;
        setTimeout(tick, restartDelay);
      }, holdDelay);
    }
  }

  render();
  tick();
}

document.addEventListener('DOMContentLoaded', () => {
  typeWordByWordWithCursor(document.getElementById('hero-typing'));
});