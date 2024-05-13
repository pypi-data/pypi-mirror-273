## -*- coding: utf-8; -*-
<%namespace file="/grids/nav.mako" import="grid_index_nav" />
<%namespace file="/autocomplete.mako" import="tailbone_autocomplete_template" />
<%namespace name="base_meta" file="/base_meta.mako" />
<%namespace file="/formposter.mako" import="declare_formposter_mixin" />
<%namespace file="/grids/filter-components.mako" import="make_grid_filter_components" />
<%namespace name="page_help" file="/page_help.mako" />
<%namespace name="multi_file_upload" file="/multi_file_upload.mako" />
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <title>${base_meta.global_title()} &raquo; ${capture(self.title)|n}</title>
    ${base_meta.favicon()}
    ${self.header_core()}

    % if background_color:
        <style type="text/css">
          body, .navbar, .footer {
              background-color: ${background_color};
          }
        </style>
    % endif

    % if not request.rattail_config.production():
        <style type="text/css">
          body, .navbar, .footer {
            background-image: url(${request.static_url('tailbone:static/img/testing.png')});
          }
        </style>
    % endif

    ${self.head_tags()}
  </head>

  <body>
    ${declare_formposter_mixin()}

    ${self.body()}

    <div id="whole-page-app">
      <whole-page></whole-page>
    </div>

    ${self.render_whole_page_template()}
    ${self.make_whole_page_component()}
    ${self.make_whole_page_app()}
  </body>
</html>

<%def name="title()"></%def>

<%def name="content_title()">
  ${self.title()}
</%def>

<%def name="header_core()">

  ${self.core_javascript()}
  ${self.extra_javascript()}
  ${self.core_styles()}
  ${self.extra_styles()}

  ## TODO: should leverage deform resources for component JS?
  ## cf. also tailbone.app.make_pyramid_config()
##   ## TODO: should this be elsewhere / more customizable?
##   % if dform is not Undefined:
##       <% resources = dform.get_widget_resources() %>
##       % for path in resources['js']:
##           ${h.javascript_link(request.static_url(path))}
##       % endfor
##       % for path in resources['css']:
##           ${h.stylesheet_link(request.static_url(path))}
##       % endfor
##   % endif
</%def>

<%def name="core_javascript()">
  ${self.vuejs()}
  ${self.buefy()}
  ${self.fontawesome()}

  ## some commonly-useful logic for detecting (non-)numeric input
  ${h.javascript_link(request.static_url('tailbone:static/js/numeric.js') + '?ver={}'.format(tailbone.__version__))}

  ## debounce, for better autocomplete performance
  ${h.javascript_link(request.static_url('tailbone:static/js/debounce.js') + '?ver={}'.format(tailbone.__version__))}

  ## Tailbone / Buefy stuff
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.buefy.datepicker.js') + '?ver={}'.format(tailbone.__version__))}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.buefy.numericinput.js') + '?ver={}'.format(tailbone.__version__))}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.buefy.oncebutton.js') + '?ver={}'.format(tailbone.__version__))}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.buefy.timepicker.js') + '?ver={}'.format(tailbone.__version__))}

  <script type="text/javascript">

    ## NOTE: this code was copied from
    ## https://bulma.io/documentation/components/navbar/#navbar-menu

    document.addEventListener('DOMContentLoaded', () => {

        // Get all "navbar-burger" elements
        const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0)

        // Add a click event on each of them
        $navbarBurgers.forEach( el => {
            el.addEventListener('click', () => {

                // Get the target from the "data-target" attribute
                const target = el.dataset.target
                const $target = document.getElementById(target)

                // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
                el.classList.toggle('is-active')
                $target.classList.toggle('is-active')

            })
        })
    })

  </script>
</%def>

<%def name="vuejs()">
  ${h.javascript_link(h.get_liburl(request, 'vue'))}
  ${h.javascript_link(h.get_liburl(request, 'vue_resource'))}
</%def>

<%def name="buefy()">
  ${h.javascript_link(h.get_liburl(request, 'buefy'))}
</%def>

<%def name="fontawesome()">
  <script defer src="${h.get_liburl(request, 'fontawesome')}"></script>
</%def>

<%def name="extra_javascript()"></%def>

<%def name="core_styles()">

  ${self.buefy_styles()}

  ${h.stylesheet_link(request.static_url('tailbone:static/css/base.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/layout.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/grids.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/grids.rowstatus.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/filters.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/forms.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/diffs.css') + '?ver={}'.format(tailbone.__version__))}

  ${h.stylesheet_link(request.static_url('tailbone:static/css/codehilite.css') + '?ver={}'.format(tailbone.__version__))}

  <style type="text/css">
    .filters .filter-fieldname,
    .filters .filter-fieldname .button {
        min-width: ${filter_fieldname_width};
        justify-content: left;
    }
    .filters .filter-verb {
        min-width: ${filter_verb_width};
    }
  </style>
</%def>

<%def name="buefy_styles()">
  % if user_css:
      ${h.stylesheet_link(user_css)}
  % else:
      ## upstream Buefy CSS
      ${h.stylesheet_link(h.get_liburl(request, 'buefy.css'))}
  % endif
</%def>

<%def name="extra_styles()"></%def>

<%def name="head_tags()"></%def>

<%def name="render_whole_page_template()">
  <script type="text/x-template" id="whole-page-template">
    <div>
      <header>

        <nav class="navbar" role="navigation" aria-label="main navigation">

          <div class="navbar-brand">
            <a class="navbar-item" href="${url('home')}"
               v-show="!globalSearchActive">
              ${base_meta.header_logo()}
              <div id="global-header-title">
                ${base_meta.global_title()}
              </div>
            </a>
            <div v-show="globalSearchActive"
                 class="navbar-item">
              <b-autocomplete ref="globalSearchAutocomplete"
                              v-model="globalSearchTerm"
                              :data="globalSearchFilteredData"
                              field="label"
                              open-on-focus
                              keep-first
                              icon-pack="fas"
                              clearable
                              @keydown.native="globalSearchKeydown"
                              @select="globalSearchSelect">
              </b-autocomplete>
            </div>
            <a role="button" class="navbar-burger" data-target="navbar-menu" aria-label="menu" aria-expanded="false">
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
            </a>
          </div>

          <div class="navbar-menu" id="navbar-menu">
            <div class="navbar-start">

              <div v-if="globalSearchData.length"
                   class="navbar-item">
                <b-button type="is-primary"
                          size="is-small"
                          @click="globalSearchInit()">
                  <span><i class="fa fa-search"></i></span>
                </b-button>
              </div>

              % for topitem in menus:
                  % if topitem['is_link']:
                      ${h.link_to(topitem['title'], topitem['url'], target=topitem['target'], class_='navbar-item')}
                  % else:
                      <div class="navbar-item has-dropdown is-hoverable">
                        <a class="navbar-link">${topitem['title']}</a>
                        <div class="navbar-dropdown">
                          % for item in topitem['items']:
                              % if item['is_menu']:
                                  <% item_hash = id(item) %>
                                  <% toggle = 'menu_{}_shown'.format(item_hash) %>
                                  <div>
                                    <a class="navbar-link" @click.prevent="toggleNestedMenu('${item_hash}')">
                                      ${item['title']}
                                    </a>
                                  </div>
                                  % for subitem in item['items']:
                                      % if subitem['is_sep']:
                                          <hr class="navbar-divider" v-show="${toggle}">
                                      % else:
                                          ${h.link_to("{}".format(subitem['title']), subitem['url'], class_='navbar-item nested', target=subitem['target'], **{'v-show': toggle})}
                                      % endif
                                  % endfor
                              % else:
                                  % if item['is_sep']:
                                      <hr class="navbar-divider">
                                  % else:
                                      ${h.link_to(item['title'], item['url'], class_='navbar-item', target=item['target'])}
                                  % endif
                              % endif
                          % endfor
                        </div>
                      </div>
                  % endif
              % endfor

            </div><!-- navbar-start -->
            ${self.render_navbar_end()}
          </div>
        </nav>

        <nav class="level" style="margin: 0.5rem auto;">
          <div class="level-left">

            ## Current Context
            <div id="current-context" class="level-item">
              % if master:
                  % if master.listing:
                      <span class="header-text">
                        ${index_title}
                      </span>
                      % if master.creatable and master.show_create_link and master.has_perm('create'):
                          <once-button type="is-primary"
                                       tag="a" href="${url('{}.create'.format(route_prefix))}"
                                       icon-left="plus"
                                       style="margin-left: 1rem;"
                                       text="Create New">
                          </once-button>
                      % endif
                  % elif index_url:
                      <span class="header-text">
                        ${h.link_to(index_title, index_url)}
                      </span>
                      % if parent_url is not Undefined:
                          <span class="header-text">
                            &nbsp;&raquo;
                          </span>
                          <span class="header-text">
                            ${h.link_to(parent_title, parent_url)}
                          </span>
                      % elif instance_url is not Undefined:
                          <span class="header-text">
                            &nbsp;&raquo;
                          </span>
                          <span class="header-text">
                            ${h.link_to(instance_title, instance_url)}
                          </span>
                      % elif master.creatable and master.show_create_link and master.has_perm('create'):
                          % if not request.matched_route.name.endswith('.create'):
                              <once-button type="is-primary"
                                           tag="a" href="${url('{}.create'.format(route_prefix))}"
                                           icon-left="plus"
                                           style="margin-left: 1rem;"
                                           text="Create New">
                              </once-button>
                          % endif
                      % endif
                      % if master.viewing and grid_index:
                          ${grid_index_nav()}
                      % endif
                  % else:
                      <span class="header-text">
                        ${index_title}
                      </span>
                  % endif
              % elif index_title:
                  % if index_url:
                      <span class="header-text">
                        ${h.link_to(index_title, index_url)}
                      </span>
                  % else:
                      <span class="header-text">
                        ${index_title}
                      </span>
                  % endif
              % endif
            </div>

            % if expose_db_picker is not Undefined and expose_db_picker:
                <div class="level-item">
                  <p>DB:</p>
                </div>
                <div class="level-item">
                  ${h.form(url('change_db_engine'), ref='dbPickerForm')}
                  ${h.csrf_token(request)}
                  ${h.hidden('engine_type', value=master.engine_type_key)}
                  <b-select name="dbkey"
                            value="${db_picker_selected}"
                            @input="changeDB()">
                    % for option in db_picker_options:
                        <option value="${option.value}">
                          ${option.label}
                        </option>
                    % endfor
                  </b-select>
                  ${h.end_form()}
                </div>
            % endif

          </div><!-- level-left -->
          <div class="level-right">

            ## Quickie Lookup
            % if quickie is not Undefined and quickie and request.has_perm(quickie.perm):
                <div class="level-item">
                  ${h.form(quickie.url, method="get")}
                  <div class="level">
                    <div class="level-right">
                      <div class="level-item">
                        <b-input name="entry"
                                 placeholder="${quickie.placeholder}"
                                 autocomplete="off">
                        </b-input>
                      </div>
                      <div class="level-item">
                        <button type="submit" class="button is-primary">
                          <span class="icon is-small">
                            <i class="fas fa-search"></i>
                          </span>
                          <span>Lookup</span>
                        </button>
                      </div>
                    </div>
                  </div>
                  ${h.end_form()}
                </div>
            % endif

            % if master and master.configurable and master.has_perm('configure'):
                % if not request.matched_route.name.endswith('.configure'):
                    <div class="level-item">
                      <once-button type="is-primary"
                                   tag="a"
                                   href="${url('{}.configure'.format(route_prefix))}"
                                   icon-left="cog"
                                   text="${(configure_button_title or "Configure") if configure_button_title is not Undefined else "Configure"}">
                      </once-button>
                    </div>
                % endif
            % endif

            ## Theme Picker
            % if expose_theme_picker and request.has_perm('common.change_app_theme'):
                <div class="level-item">
                  ${h.form(url('change_theme'), method="post", ref='themePickerForm')}
                    ${h.csrf_token(request)}
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                      <span>Theme:</span>
                      <b-select name="theme"
                                v-model="globalTheme"
                                @input="changeTheme()">
                        % for option in theme_picker_options:
                            <option value="${option.value}">
                              ${option.label}
                            </option>
                        % endfor
                      </b-select>
                    </div>
                  ${h.end_form()}
                </div>
            % endif

            <div class="level-item">
              <page-help
                % if can_edit_help:
                @configure-fields-help="configureFieldsHelp = true"
                % endif
                >
              </page-help>
            </div>

            ## Feedback Button / Dialog
            % if request.has_perm('common.feedback'):
                <feedback-form
                   action="${url('feedback')}"
                   :message="feedbackMessage">
                </feedback-form>
            % endif

          </div><!-- level-right -->
        </nav><!-- level -->
      </header>

      ## Page Title
      % if capture(self.content_title):
          <section id="content-title"
                   class="has-background-primary">
            <div style="display: flex; align-items: center; padding: 0.5rem;">

              <h1 class="title has-text-white"
                  v-html="contentTitleHTML">
              </h1>

              <div style="flex-grow: 1; display: flex; gap: 0.5rem;">
                ${self.render_instance_header_title_extras()}
              </div>

              <div style="display: flex; gap: 0.5rem;">
                ${self.render_instance_header_buttons()}
              </div>

            </div>
          </section>
      % endif

      <div class="content-wrapper">

      ## Page Body
      <section id="page-body">

        % if request.session.peek_flash('error'):
            % for error in request.session.pop_flash('error'):
                <b-notification type="is-warning">
                  ${error}
                </b-notification>
            % endfor
        % endif

        % if request.session.peek_flash('warning'):
            % for msg in request.session.pop_flash('warning'):
                <b-notification type="is-warning">
                  ${msg}
                </b-notification>
            % endfor
        % endif

        % if request.session.peek_flash():
            % for msg in request.session.pop_flash():
                <b-notification type="is-info">
                  ${msg}
                </b-notification>
            % endfor
        % endif

        ${self.render_this_page_component()}
      </section>

      ## Footer
      <footer class="footer">
        <div class="content">
          ${base_meta.footer()}
        </div>
      </footer>

      </div><!-- content-wrapper -->
    </div>
  </script>

  ${page_help.render_template()}

  % if request.has_perm('common.feedback'):
  <script type="text/x-template" id="feedback-template">
    <div>

      <div class="level-item">
        <b-button type="is-primary"
                  @click="showFeedback()"
                  icon-pack="fas"
                  icon-left="comment">
          Feedback
        </b-button>
      </div>

      <b-modal has-modal-card
               :active.sync="showDialog">
        <div class="modal-card">

          <header class="modal-card-head">
            <p class="modal-card-title">User Feedback</p>
          </header>

          <section class="modal-card-body">
            <p class="block">
              Questions, suggestions, comments, complaints, etc.
              <span class="red">regarding this website</span> are
              welcome and may be submitted below.
            </p>

            <b-field label="User Name">
              <b-input v-model="userName"
                       % if request.user:
                       disabled
                       % endif
                       >
              </b-input>
            </b-field>

            <b-field label="Referring URL">
              <b-input
                 v-model="referrer"
                 disabled="true">
              </b-input>
            </b-field>

            <b-field label="Message">
              <b-input type="textarea"
                       v-model="message"
                       ref="textarea">
              </b-input>
            </b-field>

            % if request.rattail_config.getbool('tailbone', 'feedback_allows_reply'):
                <div class="level">
                  <div class="level-left">
                    <div class="level-item">
                      <b-checkbox v-model="pleaseReply"
                                  @input="pleaseReplyChanged">
                        Please email me back{{ pleaseReply ? " at: " : "" }}
                      </b-checkbox>
                    </div>
                    <div class="level-item" v-show="pleaseReply">
                      <b-input v-model="userEmail"
                               ref="userEmail">
                      </b-input>
                    </div>
                  </div>
                </div>
            % endif

          </section>

          <footer class="modal-card-foot">
            <b-button @click="showDialog = false">
              Cancel
            </b-button>
            <once-button type="is-primary"
                         @click="sendFeedback()"
                         :disabled="!message.trim()"
                         text="Send Message">
            </once-button>
          </footer>
        </div>
      </b-modal>

    </div>
  </script>
  % endif

  ${tailbone_autocomplete_template()}
  ${multi_file_upload.render_template()}
</%def>

<%def name="render_this_page_component()">
  <this-page @change-content-title="changeContentTitle"
             % if can_edit_help:
             :configure-fields-help="configureFieldsHelp"
             % endif
             >
  </this-page>
</%def>

<%def name="render_navbar_end()">
  <div class="navbar-end">
    ${self.render_user_menu()}
  </div>
</%def>

<%def name="render_user_menu()">
  % if request.user:
      <div class="navbar-item has-dropdown is-hoverable">
        % if messaging_enabled:
            <a class="navbar-link ${'root-user' if request.is_root else ''}">${request.user}${" ({})".format(inbox_count) if inbox_count else ''}</a>
        % else:
            <a class="navbar-link ${'root-user' if request.is_root else ''}">${request.user}</a>
        % endif
        <div class="navbar-dropdown">
          % if request.is_root:
              ${h.link_to("Stop being root", url('stop_root'), class_='navbar-item root-user')}
          % elif request.is_admin:
              ${h.link_to("Become root", url('become_root'), class_='navbar-item root-user')}
          % endif
          % if messaging_enabled:
              ${h.link_to("Messages{}".format(" ({})".format(inbox_count) if inbox_count else ''), url('messages.inbox'), class_='navbar-item')}
          % endif
          % if request.is_root or not request.user.prevent_password_change:
              ${h.link_to("Change Password", url('change_password'), class_='navbar-item')}
          % endif
          ${h.link_to("Edit Preferences", url('my.preferences'), class_='navbar-item')}
          ${h.link_to("Logout", url('logout'), class_='navbar-item')}
        </div>
      </div>
  % else:
      ${h.link_to("Login", url('login'), class_='navbar-item')}
  % endif
</%def>

<%def name="render_instance_header_title_extras()"></%def>

<%def name="render_instance_header_buttons()">
  ${self.render_crud_header_buttons()}
  ${self.render_prevnext_header_buttons()}
</%def>

<%def name="render_crud_header_buttons()">
  % if master and master.viewing:
      ## TODO: is there a better way to check if viewing parent?
      % if parent_instance is Undefined:
          % if master.editable and instance_editable and master.has_perm('edit'):
              <once-button tag="a" href="${action_url('edit', instance)}"
                           icon-left="edit"
                           text="Edit This">
              </once-button>
          % endif
          % if master.cloneable and master.has_perm('clone'):
              <once-button tag="a" href="${action_url('clone', instance)}"
                           icon-left="object-ungroup"
                           text="Clone This">
              </once-button>
          % endif
          % if master.deletable and instance_deletable and master.has_perm('delete'):
              <once-button tag="a" href="${action_url('delete', instance)}"
                           type="is-danger"
                           icon-left="trash"
                           text="Delete This">
              </once-button>
          % endif
      % else:
          ## viewing row
          % if instance_deletable and master.has_perm('delete_row'):
              <once-button tag="a" href="${action_url('delete', instance)}"
                           type="is-danger"
                           icon-left="trash"
                           text="Delete This">
              </once-button>
          % endif
      % endif
  % elif master and master.editing:
      % if master.viewable and master.has_perm('view'):
          <once-button tag="a" href="${action_url('view', instance)}"
                       icon-left="eye"
                       text="View This">
          </once-button>
      % endif
      % if master.deletable and instance_deletable and master.has_perm('delete'):
          <once-button tag="a" href="${action_url('delete', instance)}"
                       type="is-danger"
                       icon-left="trash"
                       text="Delete This">
          </once-button>
      % endif
  % elif master and master.deleting:
      % if master.viewable and master.has_perm('view'):
          <once-button tag="a" href="${action_url('view', instance)}"
                       icon-left="eye"
                       text="View This">
          </once-button>
      % endif
      % if master.editable and instance_editable and master.has_perm('edit'):
          <once-button tag="a" href="${action_url('edit', instance)}"
                       icon-left="edit"
                       text="Edit This">
          </once-button>
      % endif
  % endif
</%def>

<%def name="render_prevnext_header_buttons()">
  % if show_prev_next is not Undefined and show_prev_next:
      % if prev_url:
          <b-button tag="a" href="${prev_url}"
                    icon-pack="fas"
                    icon-left="arrow-left">
            Older
          </b-button>
      % else:
          <b-button tag="a" href="#"
                    disabled
                    icon-pack="fas"
                    icon-left="arrow-left">
            Older
          </b-button>
      % endif
      % if next_url:
          <b-button tag="a" href="${next_url}"
                    icon-pack="fas"
                    icon-left="arrow-right">
            Newer
          </b-button>
      % else:
          <b-button tag="a" href="#"
                    disabled
                    icon-pack="fas"
                    icon-left="arrow-right">
            Newer
          </b-button>
      % endif
  % endif
</%def>

<%def name="declare_whole_page_vars()">
  ${page_help.declare_vars()}
  ${multi_file_upload.declare_vars()}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.feedback.js') + '?ver={}'.format(tailbone.__version__))}
  <script type="text/javascript">

    let WholePage = {
        template: '#whole-page-template',
        mixins: [FormPosterMixin],
        computed: {

            globalSearchFilteredData() {
                if (!this.globalSearchTerm.length) {
                    return this.globalSearchData
                }

                let terms = []
                for (let term of this.globalSearchTerm.toLowerCase().split(' ')) {
                    term = term.trim()
                    if (term) {
                        terms.push(term)
                    }
                }
                if (!terms.length) {
                    return this.globalSearchData
                }

                // all terms must match
                return this.globalSearchData.filter((option) => {
                    let label = option.label.toLowerCase()
                    for (let term of terms) {
                        if (label.indexOf(term) < 0) {
                            return false
                        }
                    }
                    return true
                })
            },

        },

        mounted() {
            window.addEventListener('keydown', this.globalKey)
            for (let hook of this.mountedHooks) {
                hook(this)
            }
        },
        beforeDestroy() {
            window.removeEventListener('keydown', this.globalKey)
        },

        methods: {

            changeContentTitle(newTitle) {
                this.contentTitleHTML = newTitle
            },

            % if expose_db_picker is not Undefined and expose_db_picker:
                changeDB() {
                    this.$refs.dbPickerForm.submit()
                },
            % endif

            % if expose_theme_picker and request.has_perm('common.change_app_theme'):
                changeTheme() {
                    this.$refs.themePickerForm.submit()
                },
            % endif

            globalKey(event) {

                // Ctrl+8 opens global search
                if (event.target.tagName == 'BODY') {
                    if (event.ctrlKey && event.key == '8') {
                        this.globalSearchInit()
                    }
                }
            },

            globalSearchInit() {
                this.globalSearchTerm = ''
                this.globalSearchActive = true
                this.$nextTick(() => {
                    this.$refs.globalSearchAutocomplete.focus()
                })
            },

            globalSearchKeydown(event) {

                // ESC will dismiss searchbox
                if (event.which == 27) {
                    this.globalSearchActive = false
                }
            },

            globalSearchSelect(option) {
                location.href = option.url
            },

            toggleNestedMenu(hash) {
                const key = 'menu_' + hash + '_shown'
                this[key] = !this[key]
            },
        },
    }

    let WholePageData = {
        contentTitleHTML: ${json.dumps(capture(self.content_title))|n},
        feedbackMessage: "",

        % if expose_theme_picker and request.has_perm('common.change_app_theme'):
            globalTheme: ${json.dumps(theme)|n},
        % endif

        % if can_edit_help:
            configureFieldsHelp: false,
        % endif

        globalSearchActive: false,
        globalSearchTerm: '',
        globalSearchData: ${json.dumps(global_search_data)|n},

        mountedHooks: [],
    }

    ## declare nested menu visibility toggle flags
    % for topitem in menus:
        % if topitem['is_menu']:
            % for item in topitem['items']:
                % if item['is_menu']:
                    WholePageData.menu_${id(item)}_shown = false
                % endif
            % endfor
        % endif
    % endfor

  </script>
</%def>

<%def name="modify_whole_page_vars()">
  <script type="text/javascript">

    % if request.user:
    FeedbackFormData.userUUID = ${json.dumps(request.user.uuid)|n}
    FeedbackFormData.userName = ${json.dumps(six.text_type(request.user))|n}
    % endif

  </script>
</%def>

<%def name="finalize_whole_page_vars()">
  ## NOTE: if you override this, must use <script> tags
</%def>

<%def name="make_whole_page_component()">

  ${make_grid_filter_components()}

  ${self.declare_whole_page_vars()}
  ${self.modify_whole_page_vars()}
  ${self.finalize_whole_page_vars()}

  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.buefy.autocomplete.js') + '?ver={}'.format(tailbone.__version__))}

  ${page_help.make_component()}
  ${multi_file_upload.make_component()}

  <script type="text/javascript">

    FeedbackForm.data = function() { return FeedbackFormData }

    Vue.component('feedback-form', FeedbackForm)

    WholePage.data = function() { return WholePageData }

    Vue.component('whole-page', WholePage)

  </script>
</%def>

<%def name="make_whole_page_app()">
  <script type="text/javascript">

    new Vue({
        el: '#whole-page-app'
    })

  </script>
</%def>

<%def name="wtfield(form, name, **kwargs)">
  <div class="field-wrapper${' error' if form[name].errors else ''}">
    <label for="${name}">${form[name].label}</label>
    <div class="field">
      ${form[name](**kwargs)}
    </div>
  </div>
</%def>

<%def name="simple_field(label, value)">
  ## TODO: keep this? only used by personal profile view currently
  ## (although could be useful for any readonly scenario)
  <div class="field-wrapper">
    <div class="field-row">
      <label>${label}</label>
      <div class="field">
        ${'' if value is None else value}
      </div>
    </div>
  </div>
</%def>
