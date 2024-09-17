// script.js

document.addEventListener('DOMContentLoaded', () => {
    // Função para alternar a visibilidade da lista de veículos
    function toggleVeiculosVisibility() {
        const veiculosSection = document.getElementById('Veiculos');
        if (veiculosSection.style.display === 'none' || veiculosSection.style.display === '') {
            veiculosSection.style.display = 'block';
        } else {
            veiculosSection.style.display = 'none';
        }
    }

    // Adiciona um evento de clique ao item do menu "Veículos"
    const veiculosMenuItem = document.querySelector('nav ul li a[href="veiculos.html"]');
    if (veiculosMenuItem) {
        veiculosMenuItem.addEventListener('click', (event) => {
            event.preventDefault(); // Previne o comportamento padrão do link
            toggleVeiculosVisibility();
        });
    }

    // Adiciona efeito de destaque ao passar o mouse sobre um veículo
    const blocosVeiculos = document.querySelectorAll('.blocosVeiculos');
    blocosVeiculos.forEach(bloco => {
        bloco.addEventListener('mouseover', () => {
            bloco.style.transform = 'scale(1.05)';
            bloco.style.transition = 'transform 0.3s ease';
        });

        bloco.addEventListener('mouseout', () => {
            bloco.style.transform = 'scale(1)';
        });
    });
});
