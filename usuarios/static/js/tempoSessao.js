let tempoTotal = parseInt(document.getElementById('tempoExpiraSessao').innerText); 
let tempoRestante = tempoTotal;

function atualizarTempo() {
  document.getElementById('tempoRestante').innerText = tempoRestante + ' segundos';

  if (tempoRestante <= 0) {
    window.location.href = "/auth/login/";
    alert("Sua sessão expirou. Você será redirecionado para a tela de login.");
  } else {
    tempoRestante--;
  }
}

setInterval(atualizarTempo, 1000);
