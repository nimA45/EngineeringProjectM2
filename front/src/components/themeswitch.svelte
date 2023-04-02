<script>
    import { onMount } from 'svelte';
    
    const switchTheme = (theme) => {
      document.body.classList.remove('dark', 'light', 'auto');
      document.body.classList.add(theme);
    };
  
    onMount(() => {
      const switcher = document.getElementById('theme-switcher');
      switcher.addEventListener('click', () => {
        if (document.body.classList.contains('dark')) {
          switchTheme('light');
        } else if (document.body.classList.contains('light')) {
          switchTheme('auto');
        } else {
          switchTheme('dark');
        }
      });
    });
  </script>
  
  <button id="theme-switcher" class="btn btn-outline contrast">
    <span class="icon sun"></span>
    <span class="icon moon"></span>
    <span class="icon auto"></span>
  </button>
  