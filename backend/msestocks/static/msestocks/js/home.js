// small helper to reveal animated cards on scroll
document.addEventListener('DOMContentLoaded', function(){
  const cards = document.querySelectorAll('.animated-card');
  const obs = new IntersectionObserver((entries)=>{
    entries.forEach((e)=>{
      if(e.isIntersecting){ e.target.classList.add('visible'); obs.unobserve(e.target); }
    })
  },{threshold:0.18});
  cards.forEach(c=>obs.observe(c));
});
