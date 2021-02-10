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
  # sample entry
  # '12': [5,7], i.e room_id 5 and 7 is busy during time 1 to 2
  }

  meetings = {
    # An sample entry
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
  def validate_meeting_details(self, details):
    """Checks if meeting details are valid
    - time should be in [1,24]
    - employee_id should be in [1,N], N is employees_count
    - meeting_id should exist in meetings
    - @return Boolean(True/False)
    """
    is_valid = True

    # time should be a discrete value in [1,24], end_time>start_time
    if 'start_time' in details and 'end_time' in details:
      start_time = details['start_time']
      end_time = details['end_time']
      if not type(start_time) == int or not type(end_time) == int or\
        start_time not in range(1 ,25) or end_time not in range(1, 25):
        print('Invalid time provided.')
        is_valid = False

      if start_time >= end_time:
        print('start_time should be strictly less than end_time.')
        is_valid = False
      
      if end_time - start_time > 3:
        print('Meeting should not exceed 3 hours.')
        is_valid = False

    # check if employee_id is valid
    if 'employee_id' in details:
      employee_id = details['employee_id']
      if type(employee_id) != int or employee_id not in range(1, len(self.employees_count)+1):
        print('Invalid Employee ID.')
        is_valid = False
    
    # validate meeting_id
    if 'meeting_id' in details:
      meeting_id = details['meeting_id']
      if meeting_id not in self.meetings:
        print('Invalid meeting_id.')
        is_valid = False
    
    if not is_valid:
      print('Invalid meeting details.')
      return False
    
    return True


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
    is_valid_details = self.validate_meeting_details({'employee_id': employee_id, 'start_time': start_time, 'end_time': end_time})

    if is_valid_details:
      time_key = get_time_key(start_time, end_time)

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
    # validate input
    is_valid_details = self.validate_meeting_details(self, {'employee_id': employee_id, 'meeting_id': meeting_id})

    if is_valid_details:
      # cancel the meeting if employee_id has created this meeting
      if self.meetings[meeting_id].employee_id == employee_id:
        time_key = get_time_key(start_time, end_time)
        roome_id = self.meetings[meeting_id].room_id
        self.schedules[time_key].remove(room_id) # free the room from schedules 
        del self.meetings[meeting_id] # remove meeting detail from meetings
        print('Successfuly canceled the meeting')
      else: print('You are not the organizer of this meeting')


def CreateMeetingSystem():
  valid_meeting_initializer = False
  while not valid_meeting_initializer:
    employees_count = input('Please Enter the no of employees > ')
    rooms_count = input('Please Enter the no of rooms > ')

    try:
      employees_count = int(employees_count)
      rooms_count = int(rooms_count)
      valid_meeting_initializer = True # valid a meeting initiallizers rooms_count and employees_count, stop calling initializer again now

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
          if type(employee_id) == str or type(start_time) == str or type(end_time) == str:
            print('invalid input try again ...')
          else:  
            meeting_system.book_room(int(employee_id), int(start_time), int(end_time))
        
        # Processing a cancel request
        if request_type == 'cancel':
          [employee_id, meeting_id] = input('Enter the cancelation details (employee_id meeting_id ) e.g 4 9 > ').split(' ')
          if type(employee_id) == str or type(meeting_id) == str:
            print('invalid input try again ...')
          meeting_system.book_room(int(employee_id), int(meeting_id))
        print('Currently scheduled meetings - \n', meeting_system.meetings)
    except:
        print('Invalid employees_count or rooms_count. Try again ...')


CreateMeetingSystem()