# Notes
# 1. the meeting system is designed to handle operatinos within a single day 
# 2. in a day time is measured using 24 hour clock 1,2,3...24
# 3. time inputs are allowed only as [1,2 .... 23, 24] discrete values


class MeetingSystem:
  """ A model to create a meeting system with following methods
  - book: input format = book employee_id, start_time, end_time
  - cancel: input format = cancel employee_id, meeting_id

  Helper/utitlity methods
  - get_time_key: returns a string key for given time interval
  - confirm_room: books a room with gicen details
  """
  schedules = {
  # '12': [5,7], i.e room_id 5 and 7 is busy during time 1 to 2
  }

  meetings = {
    # An sample entry in meetings dictionay
    # meeting_id: {
    #   employee_id: demo_employee_id,
    #   start_time: demo_start_time,
    #   end_time: demo_end_time,
    #   room_id: demo_room_id,
    # }
  }

  rooms_count = 0
  employees_count = 0

  # Initializing meetings system
  def __init__(self, rooms_count, employees_count):
    """ Just initiallizes the meeting system with employees_count and rooms_count
    """
    self.rooms_count = rooms_count
    self.employees_count = employees_count

  
  # Utitlity methods 
  def get_time_key(self, start_time, end_time):
    """ Helper to get string key of time interval
    - @input start_time and end_time
    - @returns string key - for this time interval
    """
    return str(start_time) + str(end_time)


  def confirm_room(self, employee_id, start_time, end_time):
    """Schedule a meeting in the first room which is free at the requested time slot
    - @input employee_id, start_time, end_time
    - @returns void
    """
    time_key = get_time_key(start_time, end_time)
    engaged_rooms = schedules[time_key]
    free_room_id = len(engaged_rooms) + 1

    # schedule a meeting in free_room_id
    # making room busy for this time interval
    if time_key not in schedules:
      schedules[time_key] = [free_room_id]
    else:
      schedules[time_key].append(free_room_id)

    # create a meeting at this time
    self.meetings[len(self.meetings) + 1] = {
      room_id: free_room_id,
      employee_id: employee_id,
      start_time: start_time,
      end_time: end_time,
    }
    print('Successfuly booked room for meeting')


  def book_room(self, employee_id, start_time, end_time):
    """Schedules a meeting in a room with requested details
    """
    time_key = get_time_key(start_time, end_time)

    # check if employee_id is valid
    if employee_id < 1 or employee_id > self.employees_count: print('No such employee.')

    # Can't book a meeting of more than 3 hours
    if end_time - start_time > 3:
      print("A meeting can't not exceed 3 hours")

    # check if there is any meetings in this time slot
    if time_key not in self.schedules:
      self.confirm_room(self, employee_id, start_time, end_time)
    else:
      # see if the employee has already a meeting at this time
      already_booked_meeting = False # suppose not booked a meeting already by this member
      for room_id in self.schedules[time_key]:
        # see if one of the room is having a meeting scheduled by employee_id
        for meeting in self.meetings:
          if meeting.start_time == start_time and meeting.end_time == end_time and meeting.employee_id == employee_id:
            already_booked_meeting = True # found a meeting booked by this employee_id at same time
            print('Employee has already a meeting scheduled at same time')

      if not already_booked_meeting:
        # even though this employee has not booked a meeting at this time, there are already other meetings going on at this time
        # see if there is a free room to schedule this meeting at this time
        engaged_rooms = self.schedules[time_key]
        if len(engaged_rooms) + 1 > self.rooms_count: # all rooms are already engaged for this time
          print('All rooms busy for the given time interval')
        else:
          self.confirm_room(self, employee_id, start_time, end_time)


  def cancel_room(self, employee_id, meeting_id):
    # check if employee_id is valid
    if employee_id < 1 or employee_id > self.employees_count: print('No such employee.')

    # check if meeting_id exists
    if meeting_id not in self.meetings: print('No such meeting.')

    # cancel the meeting if employee_id has created this meeting
    if self.meetings[meeting_id].employee_id == employee_id:
      time_key = get_time_key(start_time, end_time)
      roome_id = self.meetings[meeting_id].room_id
      self.schedules[time_key].remove(room_id) # free the room from schedules 
      del self.meetings[meeting_id] # remove meeting detail from meetings
      print('Successfuly canceled the meeting')
    else: print('You are not the organizer of this meeting')


def CreateMeetingSystem():
  employees_count = int(input('Please Enter the no of employees > '))
  rooms_count = int(input('Please Enter the no of rooms > '))
  meeting_system = MeetingSystem(rooms_count, employees_count)
  print('A MeetingSystem with %s Employees and %s meeting rooms has been created.\n'%(employees_count, rooms_count))
  
  print('Notes :-\n')
  print('1. Employee IDs should be in [1-N], N is the employee_count')
  print('2. Time should be in [1,24]\n')

  request_type = 1
  while request_type != 'quit':
    request_type = input('Enter the request_type [book, cancel, quit] > ')
    if request_type not in ['book', 'cancel', 'quit']:
      print('Operations not allowed. Please try again ...')
    
    # processing book Operations
    if request_type == 'book':
      [employee_id, start_time, end_time] = input('Enter the booking details (employee_id start_time end_time) e.g 4 2 3 > ').split(' ')
      meeting_system.book_room(employee_id, start_time, end_time)
    
    # Processing a cancel request
    if request_type == 'cancel':
      [employee_id, start_time, end_time] = input('Enter the cancelation details (employee_id meeting_id ) e.g 4 9 > ').split(' ')
      meeting_system.book_room(employee_id, meeting_id)
    
    print('Currently scheduled meetings - \n', meeting_system.meetings)


CreateMeetingSystem()