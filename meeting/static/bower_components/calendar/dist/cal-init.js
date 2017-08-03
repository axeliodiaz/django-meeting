!function($) {
    "use strict";

    var CalendarApp = function() {
        this.$body = $("body")
        this.$calendar = $('#calendar'),
        this.$event = ('#calendar-events div.calendar-events'),
        this.$categoryForm = $('#add-new-event form'),
        this.$extEvents = $('#calendar-events'),
        this.$modal = $('#my-event'),
        this.$saveCategoryBtn = $('.save-category'),
        this.$calendarObj = null
    };

    /* on click on event */
    CalendarApp.prototype.onEventClick =  function (calEvent, jsEvent, view) {
        var $this = this;
            var reservation = calEvent.reservation;
            console.log(reservation);
            var capacity = reservation.capacity;
            var date = reservation.date;
            var start = reservation.start;
            var end = reservation.end;
            var options = [];
            var supplies_selected = [];

            for (var i = 0; i < reservation.room.supplie.length; i++) {
                options.push({id: reservation.room.supplie[i].id, text: reservation.room.supplie[i].name});
            }
            for (var i = 0; i < reservation.supplie.length; i++) {
                supplies_selected.push(reservation.supplie[i].id);
            }
            $("#modal-title").text(reservation.room.name);
            $("#id_room").val(reservation.room.id).trigger('change');
            $("#id_supplie").empty().select2({data: options}).val(supplies_selected).trigger('change');
            $("#id_capacity").val(capacity);
            $("#datepicker").val(date);
            $("#id_start").val(start);
            $("#id_end").val(end);
            $("#id_reservation").val(reservation.id);
            $this.$modal.modal({
                backdrop: 'static'
            });
    },
    /* on select */
    CalendarApp.prototype.onSelect = function (start, end, allDay) {
        var $this = this;
            $this.$modal.modal({
                backdrop: 'static'
            });
            var form = $("<form></form>");
            form.append("<div class='row'></div>");
            form.find(".row")
                .append("<div class='col-md-6'><div class='form-group'><label class='control-label'>Event Name</label><input class='form-control' placeholder='Insert Event Name' type='text' name='title'/></div></div>")
                .append("<div class='col-md-6'><div class='form-group'><label class='control-label'>Category</label><select class='form-control' name='category'></select></div></div>")
                .find("select[name='category']")
                .append("<option value='bg-danger'>Danger</option>")
                .append("<option value='bg-success'>Success</option>")
                .append("<option value='bg-purple'>Purple</option>")
                .append("<option value='bg-primary'>Primary</option>")
                .append("<option value='bg-pink'>Pink</option>")
                .append("<option value='bg-info'>Info</option>")
                .append("<option value='bg-warning'>Warning</option></div></div>");
            $this.$modal.find('.delete-event').hide().end().find('.save-event').show().end().find('.modal-body').empty().prepend(form).end().find('.save-event').unbind('click').click(function () {
                form.submit();
            });
            $this.$modal.find('form').on('submit', function () {
                var title = form.find("input[name='title']").val();
                var beginning = form.find("input[name='beginning']").val();
                var ending = form.find("input[name='ending']").val();
                var categoryClass = form.find("select[name='category'] option:checked").val();
                if (title !== null && title.length != 0) {
                    $this.$calendarObj.fullCalendar('renderEvent', {
                        title: title,
                        start:start,
                        end: end,
                        allDay: false,
                        className: categoryClass
                    }, true);
                    $this.$modal.modal('hide');
                }
                else{
                    alert('You have to give a title to your event');
                }
                return false;

            });
            $this.$calendarObj.fullCalendar('unselect');
    },
    CalendarApp.prototype.enableDrag = function() {
        //init events
        $(this.$event).each(function () {
            // create an Event Object (http://arshaw.com/fullcalendar/docs/event_data/Event_Object/)
            // it doesn't need to have a start or end
            var eventObject = {
                title: $.trim($(this).text()) // use the element's text as the event title
            };
            // store the Event Object in the DOM element so we can get to it later
            $(this).data('eventObject', eventObject);
            // make the event draggable using jQuery UI
            $(this).draggable({
                zIndex: 999,
                revert: true,      // will cause the event to go back to its
                revertDuration: 0  //  original position after the drag
            });
        });
    }
    /* Initializing */
    CalendarApp.prototype.init = function() {
        this.enableDrag();
        /*  Initialize the calendar  */

        function toDateTime(dateStr, timeStr) {
            const [day, month, year] = dateStr.split("-");
            const [hour, minute, second] = timeStr.split(":");
            return new Date(day, month - 1, year, hour, minute, second);
        }

        var date = new Date();
        var d = date.getDate();
        var m = date.getMonth();
        var y = date.getFullYear();
        var form = '';
        var today = new Date($.now());

        var defaultEvents =  [];

        $.ajax({
            url : "/api/reservation/",
            dataType : 'json',
            async: false,
        }).done(function (obj) {
            var objects = obj;
            var reservations = objects.reservations;
            var user = objects.user;
            for (var i = 0; i < reservations.length; i++) {
                var label_status = 'info';
                if (reservations[i].room.status == 'available'){
                    label_status = 'success';
                } else if  (reservations[i].room.status == 'not available'){
                    label_status = 'danger';
                } else if (reservations[i].room.status == 'reserved'){
                    label_status = 'warning';
                }
                defaultEvents[i] = {
                    title: reservations[i].room.name,
                    start: toDateTime(reservations[i].date, reservations[i].start),
                    end: toDateTime(reservations[i].date, reservations[i].end),
                    user: user,
                    className: 'bg-' + label_status,
                    reservation: reservations[i]
                }
            }
        });

        var $this = this;
        $this.$calendarObj = $this.$calendar.fullCalendar({
            slotDuration: '00:15:00', /* If we want to split day time each 15minutes */
            minTime: '08:00:00',
            maxTime: '19:00:00',
            defaultView: 'month',
            handleWindowResize: true,
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay'
            },
            events: defaultEvents,
            editable: true,
            droppable: false, // this allows things to be dropped onto the calendar !!!
            eventLimit: true, // allow "more" link when too many events
            selectable: true,
            // drop: function(date) { $this.onDrop($(this), date); },
            // select: function (start, end, allDay) { $this.onSelect(start, end, allDay); },
            eventClick: function(calEvent, jsEvent, view) { $this.onEventClick(calEvent, jsEvent, view); }

        });

        $("#reservation_calendar").on('click', function(){
            $("#id_action").val("save");
        });

        $("#delete_reservation").on('click', function(){
            $("#id_action").val("delete");
        });

        //on new event
        this.$saveCategoryBtn.on('click', function(){
            var categoryName = $this.$categoryForm.find("input[name='category-name']").val();
            var categoryColor = $this.$categoryForm.find("select[name='category-color']").val();
            if (categoryName !== null && categoryName.length != 0) {
                $this.$extEvents.append('<div class="calendar-events bg-' + categoryColor + '" data-class="bg-' + categoryColor + '" style="position: relative;"><i class="fa fa-move"></i>' + categoryName + '</div>')
                $this.enableDrag();
            }

        });
    },

   //init CalendarApp
    $.CalendarApp = new CalendarApp, $.CalendarApp.Constructor = CalendarApp

}(window.jQuery),

//initializing CalendarApp
function($) {
    "use strict";
    $.CalendarApp.init()
}(window.jQuery);
