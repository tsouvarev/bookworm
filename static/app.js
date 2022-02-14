var app = Vue.createApp({
  data: function () {
    return {
      books: [],
      isLoading: true,
      new_book: {},
      new_book_errors: {},
      edited_book: {},
      edited_book_errors: {},
      show_add_form: false,
      show_edit_form: false,
    }
  },
  delimiters: ["[[", "]]"],
  mounted() {
    axios.get('/books/').then(response => {
      this.books = response.data;
      this.isLoading = false;
    });
  },
  methods: {
    create_book: function () {
      axios.post(`/books/`, this.new_book).then(response => {
        this.books.unshift(response.data);
        this.new_book_errors = {};
      }).catch(error => {
        this.new_book_errors = error.response.data.errors;
      })
    },
    edit_book: function () {
      let { id: book_id, ...data } = this.edited_book;
      axios.patch(`/books/${book_id}/`, data).then(response => {
        this.edited_book_errors = {};
        this.show_edit_form=false;
      }).catch(error => {
        this.edited_book_errors = error.response.data.errors;
      })
    },
    delete_book: function (book) {
      if (confirm(`Удалить книгу "${book.title}"?`)) {
        axios.delete(`/books/${book.id}/`).then(response => {
          this.books = this.books.filter(value => value.id != book.id);
        })
      }
    }
  }
});
app.mount('#app');

let csrf_meta_tag = document.querySelector('meta[name="csrf-token"]');
let csrf_token = csrf_meta_tag.getAttribute('content');
axios.defaults.headers.common['X-CSRF-TOKEN'] = csrf_token;
