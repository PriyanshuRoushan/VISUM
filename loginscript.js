// Toggle password visibility
document.querySelectorAll('.toggle-password').forEach(toggle => {
    toggle.addEventListener('click', () => {
      const input = toggle.previousElementSibling;
      if (input.type === 'password') {
        input.type = 'text';
        toggle.classList.remove('ri-eye-line');
        toggle.classList.add('ri-eye-off-line');
      } else {
        input.type = 'password';
        toggle.classList.remove('ri-eye-off-line');
        toggle.classList.add('ri-eye-line');
      }
    });
  });
  