import { defineStore } from 'pinia';
import axios from 'axios';

export const useVsphereStore = defineStore('mainvsphere', {
    state: () => ({
        vdesks: [],
        SearchvDesks: [],
        setVDesks: [],
        PostTitle: '',
        currentUser: undefined,
    }),

    getters: {
        TitleUser() {
            return this.PostTitle;
        },
        vDesksList() {
            return this.vdesks;
        },
        TitleDesks() {
            return "Placeholder";
        },
        loggedInUser() {
            return this.currentUser;
        },
        vdesksearch() {
            return this.vdesks;
        }
    },

    actions: {
        async fetchUserVDesks() {
            try {
                const path = 'http://localhost:8000/vdesk';
                const result = await axios.post(path, { currentUser: this.currentUser });
                this.setSearchvDesks(result.data.SearchvDesks);
                return result;
            } catch (error) {
                console.error(error);
            }
        }, 

        async fetchAllVDesks() {
            try {
                const path = 'http://localhost:8000/search';
                const result = await axios.get(path);
                this.setVDesks(result.data.setVDesks);
                return result;
            } catch (error) {
                console.error(error);
            }
        },
        async postData(username, data) {
            try {
                const path = 'http://localhost:8000/powercycle';
                const payload = {
                    currentUser: username,
                    ...data
                };
                const results = await axios.post(path, payload);
                this.setVDesks(results.data.vdesks);
                return results;
            } catch (error) {
                console.error(error);
            }
        },
        setCurrentUser(user) {
            this.currentUser = user;
        },
        setVDesks(payload) {
            this.vdesks = payload;
        },
        setSearchvDesks(payload) {
            this.SearchvDesks = payload;
        },
        setPostTitle(payload) {
            this.PostTitle = payload;
        },
    },
});
