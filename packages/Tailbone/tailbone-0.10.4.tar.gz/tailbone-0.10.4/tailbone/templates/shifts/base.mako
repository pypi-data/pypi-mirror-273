## -*- coding: utf-8; -*-
<%inherit file="/page.mako" />

<%def name="title()">${page_title}</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/timesheet.css'))}
</%def>

<%def name="edit_timetable_styles()">
  <style type="text/css">
    .timesheet .day {
        cursor: pointer;
        height: 5em;
    }
    .timesheet tr .day.modified {
        background-color: #fcc;
    }
    .timesheet tr:nth-child(odd) .day.modified {
        background-color: #ebb;
    }
    .timesheet .day .shift.deleted {
        display: none;
    }
    #day-editor .shift {
        margin-bottom: 1em;
        white-space: nowrap;
    }
    #day-editor .shift input {
        width: 6em;
    }
    #day-editor .shift button {
        margin-left: 0.5em;
    }
    #snippets {
        display: none;
    }
  </style>
</%def>

<%def name="context_menu()"></%def>

<%def name="timesheet_wrapper(with_edit_form=False, change_employee=None)">
  <div class="timesheet-wrapper">

    ${h.form(request.current_route_url(_query=False), id='filter-form')}
    ${h.csrf_token(request)}

    <table class="timesheet-header">
      <tbody>
        <tr>

          <td class="filters" rowspan="2">

            % if employee is not Undefined:
                <div class="field-wrapper employee">
                  <label>Employee</label>
                  <div class="field">
                    ${dform['employee'].serialize(text=six.text_type(employee), selected_callback='employee_selected')|n}
                  </div>
                </div>
            % endif

            % if store_options is not Undefined:
                <div class="field-wrapper store">
                  <div class="field-row">
                    <label for="store">Store</label>
                    <div class="field">
                      ${dform['store'].serialize()|n}
                    </div>
                  </div>
                </div>
            % endif

            % if department_options is not Undefined:
                <div class="field-wrapper department">
                  <div class="field-row">
                    <label for="department">Department</label>
                    <div class="field">
                      ${dform['department'].serialize()|n}
                    </div>
                  </div>
                </div>
            % endif

            <div class="field-wrapper week">
              <label>Week of</label>
              <div class="field">
                ${week_of}
              </div>
            </div>

            ${self.edit_tools()}

          </td><!-- filters -->

          <td class="menu">
            <ul id="context-menu">
              ${self.context_menu()}
            </ul>
          </td><!-- menu -->
        </tr>

        <tr>
          <td class="tools">
            <div class="grid-tools">
              <div class="week-picker" data-week="${sunday.strftime('%Y-%m-%d')}">
                <button type="button" class="nav" data-date="${prev_sunday.strftime('%Y-%m-%d')}">&laquo; Previous</button>
                <button type="button" class="nav" data-date="${next_sunday.strftime('%Y-%m-%d')}">Next &raquo;</button>
                <label>Jump to week:</label>
                ${dform['date'].serialize(extra_options={'showButtonPanel': True}, selected_callback='date_selected')|n}
              </div>
            </div><!-- grid-tools -->
          </td><!-- tools -->
        </tr>

      </tbody>
    </table><!-- timesheet-header -->

    ${h.end_form()}

    % if with_edit_form:
        ${self.edit_form()}
    % endif

    ${self.timesheet()}

    % if with_edit_form:
        ${h.end_form()}
    % endif

  </div><!-- timesheet-wrapper -->
</%def>

<%def name="timesheet(render_day=None, extra_columns=0)">
  <style type="text/css">
    .timesheet thead th {
         width: ${'{:0.2f}'.format(100.0 / (9 + extra_columns))}%;
    }
  </style>

  <table class="timesheet">
    <thead>
      <tr>
        <th>Employee</th>
        % for day in weekdays:
            <th>${day.strftime('%A')}<br />${day.strftime('%b %d')}</th>
        % endfor
        <th>Total<br />Hours</th>
        ${self.render_extra_headers()}
      </tr>
    </thead>
    <tbody>
      % for emp in sorted(employees, key=six.text_type):
          <tr data-employee-uuid="${emp.uuid}">
            <td class="employee">
              ## TODO: add link to single employee schedule / timesheet here...
              ${emp}
            </td>
            % for day in emp.weekdays:
                <td class="day">
                  % if render_day:
                      ${render_day(day)}
                  % else:
                      ${self.render_day(day)}
                  % endif
                </td>
            % endfor
            <td class="total">
              ${self.render_employee_total(emp)}
            </td>
            ${self.render_extra_cells(employee)}
          </tr>
      % endfor
      % if employee is Undefined:
          <tr class="total">
            <td class="employee">${len(employees)} employees</td>
            % for day in weekdays:
                <td></td>
            % endfor
            <td></td>
          </tr>
      % else:
          <tr>
            <td>&nbsp;</td>
            % for day in employee.weekdays:
                <td>
                  ${self.render_employee_day_total(day)}
                </td>
            % endfor
            <td>
              ${self.render_employee_total(employee)}
            </td>
            ${self.render_extra_totals(employee)}
          </tr>
      % endif
    </tbody>
  </table>
</%def>

<%def name="edit_form()"></%def>

<%def name="edit_tools()"></%def>

<%def name="render_day(day)"></%def>

<%def name="render_employee_total(employee)"></%def>

<%def name="render_employee_day_total(day)"></%def>

<%def name="render_extra_headers()"></%def>

<%def name="render_extra_cells(employee)"></%def>

<%def name="render_extra_totals(employee)"></%def>

<%def name="page_content()">
  ${self.timesheet_wrapper()}
</%def>


${parent.body()}
