<template>
  <head>
    <meta charset="utf-8" />
  </head>

  <div v-if=" loggedInUserName ">
  <div class="container" style=" padding-top: 50px;">
      <div class="row my-5 card-wrapper">
      <div
			class="col-lg-4 col-md-6 mb-4"
			v-for="(vdesk, index) in SearchvDesks"
			:key="index">
        <div class="card h-200">
            <div class="embed-responsive embed-responsive-16by9">
				<!-- Display Image -->
				<template v-if="vdesk.MachineOpt == 'Windows'">
					<div class="text-center">
						<img v-bind:src="require('@/assets/windows.png')" />
					</div>
				</template>
				<template v-if="vdesk.MachineOpt == 'Ubuntu'">
					<div class="text-center">
					    <img v-bind:src="require('@/assets/linux.png')" />
					</div>
			    </template>

          <div class="card-body">
                <!-- Display vDesk Machine Name -->
                <h4 class="card-title">
                    vDesk: {{ vdesk.MachineName }}
                </h4>
              <!-- Display vDesk Status -->
              <p class="card-text">Machine State: {{ vdesk.MachineStatus }}</p>

              <!-- Action Buttons -->
              <template v-if="vdesk.MachineStatus != 'Powered Off' && vdesk.MachineStatus != 'Running Job'">
                <button type="button" 
                        class="btn btn-outline-warning"
                        @click="postData({'vSphere':'Horizon','PowerCycle':'PowerOff', 'vDesk':vdesk})">
                        <i class="fas fa-power-off"></i></button>

                 <button type="button" 
                         class="btn btn-outline-primary" 
                         @click="postData({'vSphere':'Horizon','PowerCycle':'Restart', 'vDesk':vdesk})">
                         <i class="fas fa-recycle"></i></button>

                 <button type="button" 
                         class="btn btn-outline-danger"
                         @click="postData({'vSphere':'Horizon','PowerCycle':'Delete', 'vDesk':vdesk})">
                         <i class="fas fa-trash"></i></button>
  
              <template v-if="vdesk.MachineOpt == 'Windows'">
                <button type="button" 
                        class="btn btn-outline-info"
                        @click="openVMwareView(vdesk.HorizonServer, vdesk.DisplayName)">
                    <i class="fas fa-desktop"></i>
                </button>
              </template>
              <!-- For Linux -->
              <template v-if="vdesk.MachineOpt == 'Ubuntu'">
                  <button type="button" 
                          class="btn btn-outline-warning"
                          @click="openSSH(vdesk.HorizonServer, vdesk.DisplayName)">
                      <i class="fas fa-terminal"></i> Open SSH
                  </button>
              </template>
              </template>

              <template v-if="vdesk.MachineStatus == 'Powered Off'">
                <button type="button" 
                         class="btn btn-outline-danger"
                         @click="postData({'vSphere':'Horizon','PowerCycle':'Delete', 'vDesk':vdesk})">
                         <i class="fas fa-power-off"></i></button>
      
                <button type="button" 
                         class="btn btn-outline-danger"
                         @click="postData({'vSphere':'Horizon','PowerCycle':'Delete', 'vDesk':vdesk})">
                         <i class="fas fa-trash"></i></button>
              </template>

              <template v-if="vdesk.MachineStatus == 'Running Job'">
                <Spinner />
              </template>
              
                <!-- Footer -->
               <div class="card-footer" style="margin-top: 5px;">
                 <small small-class="text-muted" >
                   Desktop Pool: {{ vdesk.vPool }}
                 </small>
                 <br>
                   <small small-class="text-muted" >
                   Horizon Server: {{ vdesk.vCenter }}
                 </small>
               </div>
		      </div>
        </div>
      </div>
          <!-- End of Card --> 
    </div>
    </div>
</div>
  </div>
  <!-- Displayed when the user is not logged in -->
  <div v-else class="login-needed-screen">
    Logging Needed
  </div>
</template>


<script>
import { useVsphereStore } from '@/store/vsphereStore'; 
import { useMainStore } from '@/store/mainStore';
import Spinner from '@/Scripts/Spinner.vue';



export default {
  components: {
    Spinner
  },
  data() {
    return {
      account: undefined,
      containers: [],
      polling: null,
      isLoading: false 
    };
  },
  message: '',


  computed: {
    loggedInUserName() {
      const mainStore = useMainStore();
      return mainStore.loggedInUser ? mainStore.loggedInUser.name : '';
    },
    SearchvDesks() {
      return useVsphereStore().SearchvDesks;
    },
    TitleUser: {
        get() {
            return useVsphereStore().PostTitle;
        },
        set(TitleUser) {
          useVsphereStore().setPostTitle(TitleUser); 
        },
  },
  },
  methods: {
    async getContainers() {
      try {
        console.log("Fetching containers... Setting isLoading to true");
        this.isLoading = true; 
        const vsphereStore = useVsphereStore();
        vsphereStore.setCurrentUser(this.loggedInUserName);
        // Send the loggedInUserName to fetchUserVDesks method
        await vsphereStore.fetchUserVDesks(this.loggedInUserName);  // Make sure this is awaited
        console.log(this.SearchvDesks);
      } catch (error) {
        console.error('Error fetching user vDesks:', error);
      } finally {
        this.isLoading = false; 
      }
},

  async postData(data) {
    try{
      const vsphereStore = useVsphereStore();
      vsphereStore.setCurrentUser(this.loggedInUserName);
      vsphereStore.postData(data);
      vsphereStore.fetchUserVDesks(this.loggedInUserName);
      console.log(data);
    } catch (error) {
      console.error('Error posting data:', error);
    }
    },

    openVMwareView(horizonServer, displayName) {
            const encodedDisplayName = encodeURIComponent(displayName);
            const url = `vmware-view://${horizonServer}/${encodedDisplayName}`;
            window.open(url, '_blank');
        },
    openSSH() {
      const terminalUrl = window.location.origin + '/terminal'; // Assuming you have a route path named '/terminal' for the terminal view
      window.open(terminalUrl, 'SSH Terminal', 'width=800,height=600');
  },

    pollData() {
      this.polling = setInterval(this.getContainers, 10000); // Poll every 10 seconds
    },
  },

  beforeUnmount() {
    clearInterval(this.polling);
  },

  created() {
    this.$emitter.on('login', async function(account) {
      this.account = account;
    }.bind(this));
    
     if (this.loggedInUserName) {
      this.getContainers();
      this.pollData();
    }
    this.$emitter.on('logout', () => {
      console.log('logging out');
      this.account = undefined;
      this.containers = [];  // Clear containers on logout.
    });
    
    if (this.loggedInUserName) {
      this.getContainers();
      this.pollData();
    }
  },
};
</script>
