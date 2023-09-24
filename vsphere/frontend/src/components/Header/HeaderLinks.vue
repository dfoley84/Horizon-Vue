<template>
    <div class="navbar-menu">
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <a :href="github" target="_blank" rel="noopener noreferrer">
              <i class="fab fa-github fa-2x" aria-hidden="true"></i>
            </a>
            <a :href="twitter" target="_blank" rel="noopener noreferrer">
              <i class="fab fa-twitter fa-2x" aria-hidden="true"></i>
            </a>
            <a v-if="!loggedInUser" @click="SignIn" target="_blank" rel="noopener noreferrer" class="header-icon">
              <i class="fas fa-sign-in-alt fa-2x" aria-hidden="false"></i>
            </a>
            <a v-else @click="SignOut" target="_blank" rel="noopener noreferrer" class="header-icon">
              <i class="fas fa-sign-out-alt fa-2x" aria-hidden="false"></i>
            </a>
            <div v-if="loggedInUser" class="header-icon user-text">{{ loggedInUser.name }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { useMainStore } from '@/store/mainStore';
  
  export default {
    name: 'HeaderBar',
    data() {
      return {
        github: 'https://github.com/cmatskas',
        twitter: 'https://twitter.com/christosmatskas',
      };
    },
    
    computed: {
      loggedInUser() {
        const mainStore = useMainStore();
        return mainStore.loggedInUser;
      }
    },
  
  async created() {
    const mainStore = useMainStore();
    this.$msalInstance = mainStore.msalInstance;

    if (!this.$msalInstance) {
      console.error("MSAL instance is not initialized");
      return;
    }

    try {
      await this.$msalInstance.initialize();
    } catch (error) {
      console.error("Error initializing MSAL instance:", error);
    }
  },
  
    mounted() {
      if (!this.$msalInstance) {
        console.error("MSAL instance is missing in mounted.");
        return;
      }
      const accounts = this.$msalInstance.getAllAccounts();
      if (accounts.length == 0) {
        return;
      }
      const mainStore = useMainStore();
      mainStore.setUser(accounts[0]);
    },
  
    methods: {
      async SignIn() {
      const mainStore = useMainStore();
      
      if (!this.$msalInstance) {
        console.error("MSAL instance is not initialized");
        return;
      }

      try {
        await this.$msalInstance.loginPopup({});
        const myAccounts = this.$msalInstance.getAllAccounts();
        mainStore.setUser(myAccounts[0]);
      } catch (error) {
        console.error(`error during authentication: ${error}`);
      }
    },
  
      async SignOut() {
        const mainStore = useMainStore();
  
        if (!this.$msalInstance) {
          console.error("MSAL instance is not initialized");
          return;
        }
  
        try {
          await this.$msalInstance.logoutPopup({});
          mainStore.clearUser();
        } catch (error) {
          console.error(`error during logout: ${error}`);
        }
      },
    },
  };
  </script>
  