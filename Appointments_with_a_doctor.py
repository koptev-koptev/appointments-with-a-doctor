from datetime import timedelta, datetime, time


'''Start and stop of the working day'''
work_time = [{'start' : time(9, 0), 'stop' : time(21, 0)}]

'''Start and stop intervals when appointments are impossible'''
busy = [
{'start' : time(10, 30), 'stop' : time(10, 50)},
{'start' : time(18, 40), 'stop' : time(18, 50)},
{'start' : time(14, 40), 'stop' : time(15, 50)},
{'start' : time(16, 40), 'stop' : time(17, 20)},
{'start' : time(20, 5), 'stop' : time(20, 20)}
]

'''Service duration'''
service_duration = timedelta(minutes=25)
'''Appointment interval duration'''
intervals = timedelta(minutes=30)


def get_result(work_time, busy, service_duration, interval) -> list:
    '''A program for automatically calculating windows for making appointments
       with a doctor, taking into intervals when appointments are impossible'''
    slots = []
    result = []
    slot_interval = timedelta(minutes=5)

    for idx, time_obj in enumerate(work_time):
        time_start = timedelta(hours=time_obj['start'].hour, minutes=time_obj['start'].minute)
        time_end = timedelta(hours=time_obj['stop'].hour, minutes=time_obj['stop'].minute)

        while time_end > time_start:
            slots.append(1)
            time_start += slot_interval

        if time_obj is not work_time[-1]:
            next_time = work_time[idx + 1]
            next_start_time = timedelta(hours=next_time['start'].hour, minutes=next_time['start'].minute)
            while next_start_time > time_end:
                slots.append(0)
                time_end += slot_interval

    work_start_time = timedelta(hours=work_time[0]['start'].hour, minutes=work_time[0]['start'].minute)
    for reserve in busy:
        reserve_start = timedelta(hours=reserve['start'].hour, minutes=reserve['start'].minute)
        reserve_end = timedelta(hours=reserve['stop'].hour, minutes=reserve['stop'].minute)
        reserve_idx = (reserve_start - work_start_time) // slot_interval
        while reserve_end > reserve_start:
            slots[reserve_idx] = 0
            reserve_start += slot_interval
            reserve_idx += 1

    need_slots = int(service_duration / slot_interval)
    add_pos = int(interval // slot_interval)
    for idx, slot in enumerate(slots):
        if slot == 1:
            sm = sum(slots[idx:min(len(slots), idx + need_slots)])
            if sm >= need_slots:
                if idx % add_pos == 0:
                    result.append((datetime.min + work_start_time + slot_interval * idx).time())

    return result


if __name__ == '__main__':
    work_times = get_result(work_time, busy, service_duration, intervals)
    for time in work_times:
        print(time)
