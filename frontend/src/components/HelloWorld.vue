<template>
  <head>
    <meta charset="utf-8">
    <meta name="user" content="{{ account.name }}">

  </head>
  <div class="container" style=" padding-top: 50px;">
    <!-- Display vDesk if Users Logged In-->
    <div v-if="account">
      <div hidden>
      <input v-bind="TitleUser" />
      {{ TitleUser = account.name }}
      </div>

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
                           class="btn btn-outline-info">
                           <i class="fas fa-desktop"></i></button>
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
    <div v-else>You need to authenticate to access your vDesk data</div>
  </div>
</template>

<script>
import customTokenCredential from '../CustomTokenProvider';
import { BlobServiceClient } from '@azure/storage-blob';
import { PublicClientApplication } from '@azure/msal-browser';
import { mapMutations, mapState, mapActions} from 'vuex';
const storageAccountName = 'cmatskasbackup';

export default {
  name: 'HelloWorld',
  data() {
    return {
      account: undefined,
      containers: [],
      polling: null,  
    };
  },
 message: '',

 computed:{
  ...mapState(['SearchvDesks']),

  TitleUser:{
    set(TitleUser) {
      this.$store.commit('PostTitle', TitleUser);
    },
  },
},
  async created() {
    this.pollData();
    this.$emitter.on(
      'login', async function (account) {
        this.account = account;
      }.bind(this),
    ),
      this.$emitter.on('logout', () => {
        console.log('logging out');
        this.account = undefined;
      });
  },

  methods: {
    ...mapActions(['postData']),
    ...mapMutations(['setAccessToken']),

    async getAzureStorageData() {
      if(this.$store.state.accessToken == ''){
        await this.getAccessToken();
      }
      let tokenCredential = new customTokenCredential(this.$store.state.accessToken);
      const blobClient = new BlobServiceClient(
        `https://${storageAccountName}.blob.core.windows.net`,
        tokenCredential,
      );

      let i = 1;
      const iter = blobClient.listContainers();
      let containerItem = await iter.next();
      while (!containerItem.done) {
        console.log(`Container ${i++}: ${containerItem.value.name}`);
        this.containers.push({
          id: containerItem.value.properties.etag,
          name: containerItem.value.name,
        });
        containerItem = await iter.next();
      }
    },
    async getAccessToken(){
      let request = {
        scopes: ['https://storage.azure.com/user_impersonation'],
      };
      const msalInstance = new PublicClientApplication(
        this.$store.state.msalConfig,
      );
      try {
        let tokenResponse = await msalInstance.acquireTokenSilent(request);
        this.$store.commit('setAccessToken', tokenResponse.accessToken);
      } catch (error) {
          console.error( 'Silent token acquisition failed. Using interactive mode' );
          let tokenResponse = await msalInstance.acquireTokenPopup(request);
          console.log(`Access token acquired via interactive auth ${tokenResponse.accessToken}`)
          this.$store.commit('setAccessToken',tokenResponse.accessToken);
      }
    },
    pollData() {
    this.polling = setInterval(() => {
      this.$store.dispatch('FetchUservDesks', this.payload)
    },12000)
  },
},
};
</script>
