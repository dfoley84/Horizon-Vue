<template>
    <header>
      <nav
        class="navbar has-background-dark is-dark"
        role="navigation"
        aria-label="main navigation">
        <HeaderBarBrand />
        <HeaderBarLinks />
      </nav>
    </header>
  </template>
  
  <script>
  import HeaderBarBrand from '@/components/Header/Headerband';
  import HeaderBarLinks from '@/components/Header/HeaderLinks';
  
  export default {
    name: 'HeaderBar',
    components: { HeaderBarBrand, HeaderBarLinks },
  };
  </script>
  