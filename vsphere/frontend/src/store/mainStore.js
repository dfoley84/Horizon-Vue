import { defineStore } from 'pinia';
import { PublicClientApplication } from '@azure/msal-browser';
import customTokenCredential from '@/Scripts/CustomTokenProvider';
import { BlobServiceClient } from '@azure/storage-blob';
const storageAccountName = 'cmatskasbackup';

const msalConfig = {
    auth: {
        clientId: "<CLIENTID>",
        authority: "https://login.microsoftonline.com/<TENANTID>",
    },
    cache: {
        cacheLocation: 'localStorage',
    }
};
export const useMainStore = defineStore('mainauth', {
    state: () => ({
        currentUser: null,
        userImage: null,
        accessToken: "",
        msalConfig: msalConfig,
        msalInstance: new PublicClientApplication(msalConfig)
    }),
    
    getters: {
        loggedInUser() {
            return this.currentUser;
        },
        userProfileImage() {
            return this.userImage;
        }
    },

    actions: {
        async getAzureStorageData() {
            if (this.accessToken === '') {
                await this.getAccessToken();
            }
            let tokenCredential = new customTokenCredential(this.accessToken);
            const blobClient = new BlobServiceClient(
                `https://${storageAccountName}.blob.core.windows.net`,
                tokenCredential,
            );
            let i = 1;
            const iter = blobClient.listContainers();
            let containerItem = await iter.next();
            const containers = []; 
            while (!containerItem.done) {
                console.log(`Container ${i++}: ${containerItem.value.name}`);
                containers.push({
                    id: containerItem.value.properties.etag,
                    name: containerItem.value.name,
                });
                containerItem = await iter.next();
            }
            return containers; 
        },

        async getAccessToken(){
            console.log('Attempting to get access token...'); 
            let request = {
              scopes: ['https://storage.azure.com/user_impersonation','https://graph.microsoft.com/Group.Read.All'],
            };
            
            try {
              let tokenResponse = await this.msalInstance.acquireTokenSilent(request);
              this.commit('setAccessToken', tokenResponse.accessToken);
              // Fetch user groups after successfully acquiring the token
              this.getUserGroups();
            } catch (error) {
                console.error( 'Silent token acquisition failed. Using interactive mode' );
                let tokenResponse = await this.msalInstance.acquireTokenPopup(request);
                console.log(`Access token acquired via interactive auth ${tokenResponse.accessToken}`)
                this.commit('setAccessToken',tokenResponse.accessToken);
            }
          },
          async getUserGroups() {
            console.log('Getting user groups');
            const headers = new Headers();
            const bearer = `Bearer ${this.accessToken}`;
            headers.append("Authorization", bearer);
            const options = {
                method: "GET",
                headers: headers,
            };
            const graphEndpoint = "https://graph.microsoft.com/v1.0/me/memberOf";
            try {
                const response = await fetch(graphEndpoint, options);
                const data = await response.json();
                console.log(data);
                return data.value; 
            } catch (error) {
                console.error(error);
                return [];
            }
        },

        setAccessToken(token) {
            this.accessToken = token;
        },
        setUser(user) {
            this.currentUser = user;
        },
        clearUser() {
            this.currentUser = null;
        }
    }
});