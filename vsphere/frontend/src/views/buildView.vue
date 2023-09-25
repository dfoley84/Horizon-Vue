<template>
  <div class="container">
    <div class="form-wrapper">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="requester">Requester:</label>
          <input type="text" id="requester" v-model="form.requester" />
        </div>

        <div class="form-group">
          <label for="machinename">Machine Name:</label>
          <input type="text" id="machinename" v-model="form.machinename" />
        </div>

        <div class="form-group">
          <label for="server">Server:</label>
          <input type="text" id="server" v-model="form.server" />
        </div>

        <div class="form-group">
          <label for="poolname">Pool Name:</label>
          <input type="text" id="poolname" v-model="form.poolname" />
        </div>

        <button class="submit-btn" type="submit">Submit</button>
      </form>
    </div>
  </div>
</template>



<script>
export default {
  data() {
    return {
      form: {
        requester: '',
        poolname: '',
        machinename: '',
        server: ''
      }
    }
  },
  methods: {
    handleSubmit() {
      console.log(this.form);  // Here you can process the form data
    }
  }
}
</script>