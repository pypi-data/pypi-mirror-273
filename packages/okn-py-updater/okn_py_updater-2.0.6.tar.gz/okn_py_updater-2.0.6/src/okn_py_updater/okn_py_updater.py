import collections
import math

import numpy as np
# from scipy.signal import medfilt
import statistics


def live_dispatch_function(filter_config_info, data_dict_input, pre_x_nom=0, pre_y_nom=0, pre_time=0, n_value=5):
    match_item = filter_config_info["function"]
    # print(f"Dispatched function name: {match_item}")
    if match_item == 'cdp_direction':
        # t = data_dict_input[filter_config_info["input"]]
        # # need to be fixed ********
        # keyname = "need to be fixed"
        # f = cdp_direction(config_info.log, keyname, t)
        # data_dict_input[filter_config_info["output"]] = f
        print(f"{match_item} will be coming soon.")

    elif match_item == 'reduce':
        print(f"{match_item} will be coming soon.")
        # print('reduce')

    elif match_item == 'dwnsample':
        # Implement as data drop rate in live updater
        pass

    elif match_item == 'detectblinkV':
        # x1 = data_dict_input[filter_config_info["input"][0]]
        # x2 = data_dict_input[filter_config_info["input"][1]]
        # x1 = medfilt(x1, 3)
        # x2 = medfilt(x2, 3)
        # Not tested in live updater
        pass

    elif match_item == 'deblinker2':
        # x0 = data_dict_input[filter_config_info["input"][0]]
        # y0 = data_dict_input[filter_config_info["input"][1]]
        # th = filter_config_info["threshold"]
        #
        # i = deblinker2(x0, y0, th)
        # data_dict_input[filter_config_info["output"]] = i
        # Not tested in live updater
        pass

    elif match_item == 'passthrough':
        f = data_dict_input[filter_config_info["input"]]
        output_column = filter_config_info["output"]
        data_dict_input[output_column] = f
        # print(f"{output_column} column has been added to output data.")

    elif match_item == 'dshift':
        # f = data_dict_input[filter_config_info["input"][0]]
        # data_dict_input[filter_config_info["output"]] = dshift(f)
        # Not tested in live updater
        pass

    elif match_item == 'tidy':
        # f = data_dict_input[filter_config_info["input"][0]]
        # n = filter_config_info["value"]
        # thicken = filter_config_info["thicken"]
        #
        # is_tracking = data_dict_input[filter_config_info["input"][1]]
        # data_dict_input[filter_config_info["output"]] = tidy(f, n, thicken, np.logical_not(is_tracking))
        # Not tested in live updater
        pass

    elif match_item == 'wavelet':
        # f = data_dict_input[filter_config_info["input"][0]]
        # if are_all_elements_nan(f):
        #     data_dict_input[filter_config_info["output"]] = f
        #     return
        #
        # level_for_reconstruction = np.array(filter_config_info["levelForReconstruction"])
        # wavelet_type = filter_config_info["type"]
        # level = filter_config_info["Level"]
        # data_dict_input[filter_config_info["output"]] = waveleter(f, level_for_reconstruction, wavelet_type, level)
        # Not tested in live updater
        pass

    elif match_item == 'spikeRemover':
        # Not tested in live updater
        pass

    elif match_item == 'deblinker':
        # Not tested in live updater
        pass

    elif match_item == 'shiftSignal':
        # Not tested in live updater
        pass

    elif match_item == 'medianFilter':
        input_column = filter_config_info["input"][0]
        f = data_dict_input[input_column]
        n = filter_config_info["npoint"]
        if n <= 1:
            raise ValueError("Median Filter: kernel value n must be greater than 1.")
        elif n % 2 == 0:
            raise ValueError("Median Filter: kernel value n must be odd number.")
        if len(f) >= n:
            last_n_number_array = f[:n]
            median_value = statistics.median(last_n_number_array)
            f[0] = median_value
            data_dict_input[filter_config_info["output"]] = f
        else:
            data_dict_input[filter_config_info["output"]] = f

    elif match_item == 'replaceNanBy':
        input_column = filter_config_info["input"][0]
        input_array = data_dict_input[input_column]
        pointer = filter_config_info["pointer"]
        data_dict_input[filter_config_info["output"]] = replace_nan_by(data_dict_input, input_array, pointer)

    elif match_item == 'applymask':
        # Not tested in live updater
        pass

    elif match_item == 'detrender':
        # Not tested in live updater
        pass

    elif match_item == 'detectblinkV':
        # Not tested in live updater
        pass

    elif match_item == 'gradient':
        related_column_name_array = filter_config_info["input"]
        f = data_dict_input[related_column_name_array[1]]
        t = data_dict_input[related_column_name_array[0]]
        output_column = filter_config_info["output"]
        # o = data_dict_input[output_column]
        # data_dict_input[output_column] = live_gradient(f, t, o)
        if len(f) >= n_value + 2:
            if "updated_x" in related_column_name_array[1]:
                f0 = pre_x_nom
                # t0 = pre_time
                start_index = int((n_value - 3) / 2)
                end_index = start_index + 2
                t0 = t[start_index]
                n_array = f[1:n_value + 1]
                f2 = statistics.median(n_array)
                t2 = t[end_index]
                out_array = data_dict_input[output_column]
                try:
                    out_array[0] = (f2 - f0) / (t2 - t0)
                except ZeroDivisionError:
                    out_array[0] = 0
                # out_array[0] = (f2 - f0) / (t[1] - pre_time)
                data_dict_input[output_column] = out_array
            elif "updated_y" in related_column_name_array[1]:
                f0 = pre_y_nom
                start_index = int((n_value - 3) / 2)
                end_index = start_index + 2
                t0 = t[start_index]
                n_array = f[1:n_value + 1]
                f2 = statistics.median(n_array)
                t2 = t[end_index]
                out_array = data_dict_input[output_column]
                try:
                    out_array[0] = (f2 - f0) / (t2 - t0)
                except ZeroDivisionError:
                    out_array[0] = 0
                # out_array[0] = (f2 - f0) / (t[1] - pre_time)
                data_dict_input[output_column] = out_array
    else:
        print(f"Function:{match_item} is not found")

    return data_dict_input


# def spike_remover(f):
#     pass


# def xdetectblink(x1, V, fps, varargin):
#     pass


# def detectblinkV(t, V, fps, varargin):
#     pass


def dwnsample(dict_input, number_of_reduction):
    f = len(dict_input[next(iter(dict_input))])
    number_of_reduction = int(number_of_reduction)
    if isinstance(number_of_reduction, int):
        loop_count = 0
        while loop_count < number_of_reduction:
            loop_count += 1
            for key in dict_input:
                temp_array = dict_input[key]
                temp_array = temp_array[0:f:2]
                dict_input[key] = temp_array
    else:
        print("The number of loop input must be number!")

    return dict_input


def replace_nan_by(y, input_array, pointer):
    if "<=" in pointer:
        try:
            column_name, value = str(pointer).split("<=")
            pointer_column__array = y[column_name]
            array_length = len(input_array)
            for ind in range(array_length):
                if float(pointer_column__array[ind]) <= float(value):
                    input_array[ind] = np.nan
        except KeyError:
            pass
    elif "==" in pointer:
        try:
            column_name, value = str(pointer).split("==")
            pointer_column__array = y[column_name]
            array_length = len(input_array)
            for ind in range(array_length):
                if float(pointer_column__array[ind]) == float(value):
                    input_array[ind] = np.nan
        except KeyError:
            pass
    elif ">=" in pointer:
        try:
            column_name, value = str(pointer).split(">=")
            pointer_column__array = y[column_name]
            array_length = len(input_array)
            for ind in range(array_length):
                if float(pointer_column__array[ind]) >= float(value):
                    input_array[ind] = np.nan
        except KeyError:
            pass
    else:
        if ">" in pointer:
            try:
                column_name, value = str(pointer).split(">")
                pointer_column__array = y[column_name]
                array_length = len(input_array)
                for ind in range(array_length):
                    if float(pointer_column__array[ind]) > float(value):
                        input_array[ind] = np.nan
            except KeyError:
                pass
        elif "<" in pointer:
            try:
                column_name, value = str(pointer).split("<")
                pointer_column__array = y[column_name]
                array_length = len(input_array)
                for ind in range(array_length):
                    if float(pointer_column__array[ind]) < float(value):
                        input_array[ind] = np.nan
            except KeyError:
                pass
        else:
            pass

    return input_array


def waveleter(x, level_for_reconstruction, wavelet_type, level):
    [x1, i] = fillmissing(x)
    x11 = x1

    return x11


def deblinker2(x, y, th):
    s = x * y
    i = (s > th)
    return i


def applymask(f, is_mask):
    pass


def deblinker(f, is_blinking):
    pass


def medianfilter(f, npoint):
    pass


def tidy(f, npoint, n_thicken, is_deleted):
    # need  to be fixed
    return f


def dshift(f):
    y = np.nanmean(f)
    f1 = f - y
    return f1


# def grad(f, t):
#     try:
#         df = np.gradient(f)
#         dt = np.gradient(t)
#         dfdt = df / dt
#         # print("dfdt", dfdt)
#         for ind, value in enumerate(dfdt):
#             if math.isinf(value):
#                 dfdt[ind] = 0
#             if np.isnan(value):
#                 dfdt[ind] = 0
#         return dfdt
#     except ValueError:
#         return 0
#     except RuntimeWarning:
#         return 0


# def live_gradient(f, t, out_array):
#     # print("live grad")
#     # print(f)
#     # print(t)
#     # print(out_array)
#     f_length = len(f)
#     t_length = len(t)
#     if f_length == t_length:
#         if f_length < 3:
#             if f_length <= 0:
#                 pass
#             else:
#                 return out_array
#         else:
#             max_index = f_length - 1
#             mid_index = f_length - 2
#             min_index = f_length - 3
#             df = (f[max_index] - f[min_index]) / 2
#             dt = (t[max_index] - t[min_index]) / 2
#             dfdt = df / dt
#             # print(dfdt)
#             out_array[mid_index] = dfdt
#             # print("Grad", out_array)
#             return out_array
#     else:
#         raise ValueError("Displacement and time array lengths must be the same.")


# def live_gradient(f, t):
#     f_length = len(f)
#     t_length = len(t)
#     if f_length == t_length:
#         if f_length > 0:
#             data_info_array = []
#             for pos, time in zip(f, t):
#                 temp_dict = {}
#                 temp_dict["position"] = float(pos)
#                 temp_dict["time"] = float(time)
#                 data_info_array.append(temp_dict)
#             info_array_length = len(data_info_array)
#             if info_array_length > 2:
#                 return_array = []
#                 for ind in range(info_array_length):
#                     if ind == 0:
#                         return_array.append(0)
#                     elif ind == 1:
#                         edge_grad_val = grad_by_edge_equation(data_info_array[0],
#                                                               data_info_array[1])
#                         return_array.append(edge_grad_val)
#                     else:
#                         interior_grad_val = grad_by_interior_equation(data_info_array[ind - 2],
#                                                                       data_info_array[ind - 1],
#                                                                       data_info_array[ind])
#                         return_array.append(interior_grad_val)
#                 return return_array
#             else:
#                 if info_array_length == 2:
#                     edge_grad_val = grad_by_edge_equation(data_info_array[0],
#                                                           data_info_array[1])
#                     return [0, edge_grad_val]
#                 else:
#                     if info_array_length == 1:
#                         return [0]
#                     else:
#                         pass
#     else:
#         raise ValueError("Displacement and time array lengths must be the same.")


def grad_by_edge_equation(first_ele, second_ele):
    displacement = second_ele["position"] - first_ele["position"]
    time_diff = second_ele["time"] - first_ele["time"]
    return displacement / time_diff


def grad_by_interior_equation(first_ele, second_ele, third_ele):
    hs = third_ele["time"] - second_ele["time"]
    hd = second_ele["time"] - first_ele["time"]
    f2 = third_ele["position"]
    f1 = second_ele["position"]
    f0 = first_ele["position"]
    return ((np.square(hs) * f2) + ((np.square(hd) - np.square(hs)) * f1) - (np.square(hd) * f0)) / (
            hs * hd * (hd + hs))


def cdp_direction(logs, fname, t):
    return t


def are_all_elements_nan(input_array):
    for ele in input_array:
        if not np.isnan(ele):
            return False
    return True


def fillmissing(input_array):
    # input_array = ma.masked_array(input_array, input_array == np.nan)
    # for shift in (-1, 1):
    #     for axis in (0, 1):
    #         shifted_array = np.roll(input_array, shift=shift, axis=axis)
    #         idx = ~shifted_array.mask * input_array.mask
    #         input_array[idx] = shifted_array[idx]
    return input_array


def get_out_header_array(header_array_input, filter_config_input):
    data_id_array = ["id"]
    output_header_array = [header for header in header_array_input]
    output_header_array = data_id_array + output_header_array
    for filter_info in filter_config_input:
        if filter_info["Enabled"]:
            try:
                output_header = filter_info["output"]
            except KeyError:
                output_header = None
            if output_header is not None:
                if output_header not in output_header_array:
                    output_header_array.append(output_header)

    return output_header_array


class Updater:
    def __init__(self, config, circular_buffer_length, header_array, drop_rate=0):
        if type(config) is not dict:
            raise ValueError("The config input must be dictionary type.")
        try:
            filter_config = config["filters"]
        except KeyError:
            raise KeyError("The config info does not contain filter info.")
        if type(circular_buffer_length) is not int:
            raise ValueError("The circular buffer length input must be integer type.")
        if circular_buffer_length < 3:
            raise ValueError("The circular buffer length must be at least 3.")
        if type(header_array) is not list:
            raise ValueError("The header array input must be list type.")
        if not header_array:
            raise ValueError("The header array input must not be empty.")
        if type(drop_rate) is not int:
            raise ValueError("The drop rate input must be integer type.")
        for header in header_array:
            if type(header) is not str:
                raise ValueError("The header_array element must be string.")

        self.config = config
        self.filter_config = filter_config
        self.circular_buffer = collections.deque(maxlen=circular_buffer_length)
        self.buffer_max_length = circular_buffer_length
        self.header_array = header_array
        self.out_header_array = get_out_header_array(header_array, filter_config)
        self.data_drop_rate = drop_rate
        self.currently_working_function = ['passthrough', 'medianFilter', 'replaceNanBy', 'gradient']
        self.count = 0
        self.data_id = 1
        self.pre_x_nom = 0
        self.pre_y_nom = 0
        self.pre_time = 0
        self.n_value = 5
        for filter_info in self.filter_config:
            if filter_info["Enabled"]:
                function_name = filter_info["function"]
                if function_name not in self.currently_working_function:
                    if function_name == 'dwnsample':
                        print(f"The function \"dwnsample\" is implemented as drop rate in live updater.")
                    else:
                        print(f"The function \"{function_name}\" is not available in live updater.")
                else:
                    if function_name == 'medianFilter':
                        n_point = filter_info["npoint"]
                        self.n_value = n_point
            else:
                pass

    def update(self, data_input):
        if self.data_drop_rate == 0:
            data_input.insert(0, self.data_id)
            self.data_id += 1
            temp_dict = {}
            for header_index, header_name in enumerate(self.out_header_array):
                try:
                    temp_dict[header_name] = data_input[header_index]
                except IndexError:
                    temp_dict[header_name] = 0
            data_dict = {}
            for header in self.out_header_array:
                data_dict[header] = []

            self.circular_buffer.append(temp_dict)
            for header in data_dict:
                for data in self.circular_buffer:
                    data_dict[header].append(data[header])

            # if len(self.circular_buffer) >= 3:
            for filter_info in self.filter_config:
                if filter_info["Enabled"]:
                    data_dict = live_dispatch_function(filter_info,
                                                       data_dict,
                                                       pre_x_nom=self.pre_x_nom,
                                                       pre_y_nom=self.pre_y_nom,
                                                       pre_time=self.pre_time,
                                                       n_value=self.n_value)

            converting_array = []
            for index in range(len(data_dict[self.out_header_array[0]])):
                temp_dict = {}
                for header in self.out_header_array:
                    temp_dict[header] = (data_dict[header][index])
                converting_array.append(temp_dict)

            for d_dict in self.circular_buffer:
                d_id = d_dict["id"]
                for con_dict in converting_array:
                    con_id = con_dict["id"]
                    if d_id == con_id:
                        for att in d_dict:
                            d_dict[att] = con_dict[att]
                        break

            first_data = self.circular_buffer[0]
            self.pre_x_nom = first_data["updated_x_nom"]
            self.pre_y_nom = first_data["updated_y_nom"]
            self.pre_time = first_data["record_timestamp"]
            n_data_index = int((self.n_value - 3) / 2) + 1
            n_related_data = self.circular_buffer[n_data_index]
            first_data["x_nom"] = n_related_data["x_nom"]
            first_data["y_nom"] = n_related_data["y_nom"]
            first_data["record_timestamp"] = n_related_data["record_timestamp"]
            first_data["sensor_timestamp"] = n_related_data["sensor_timestamp"]
            first_data["direction"] = n_related_data["direction"]
            out_array = []
            for header in self.out_header_array:
                out_array.append(first_data[header])
            return out_array
        else:
            if self.count == 0:
                data_input.insert(0, self.data_id)
                self.data_id += 1
                temp_dict = {}
                for header_index, header_name in enumerate(self.out_header_array):
                    try:
                        temp_dict[header_name] = data_input[header_index]
                    except IndexError:
                        temp_dict[header_name] = 0
                data_dict = {}
                for header in self.out_header_array:
                    data_dict[header] = []

                self.circular_buffer.append(temp_dict)
                for header in data_dict:
                    for data in self.circular_buffer:
                        data_dict[header].append(data[header])

                # if len(self.circular_buffer) >= 3:
                for filter_info in self.filter_config:
                    if filter_info["Enabled"]:
                        data_dict = live_dispatch_function(filter_info,
                                                           data_dict,
                                                           pre_x_nom=self.pre_x_nom,
                                                           pre_y_nom=self.pre_y_nom,
                                                           pre_time=self.pre_time,
                                                           n_value=self.n_value)

                converting_array = []
                for index in range(len(data_dict[self.out_header_array[0]])):
                    temp_dict = {}
                    for header in self.out_header_array:
                        temp_dict[header] = (data_dict[header][index])
                    converting_array.append(temp_dict)

                for d_dict in self.circular_buffer:
                    d_id = d_dict["id"]
                    for con_dict in converting_array:
                        con_id = con_dict["id"]
                        if d_id == con_id:
                            for att in d_dict:
                                d_dict[att] = con_dict[att]
                            break

                self.count = 1
                if len(self.circular_buffer) == self.buffer_max_length:
                    first_data = self.circular_buffer[0]
                    self.pre_x_nom = first_data["updated_x_nom"]
                    self.pre_y_nom = first_data["updated_y_nom"]
                    self.pre_time = first_data["record_timestamp"]
                    n_data_index = int((self.n_value - 3) / 2) + 1
                    n_related_data = self.circular_buffer[n_data_index]
                    first_data["x_nom"] = n_related_data["x_nom"]
                    first_data["y_nom"] = n_related_data["y_nom"]
                    first_data["record_timestamp"] = n_related_data["record_timestamp"]
                    first_data["sensor_timestamp"] = n_related_data["sensor_timestamp"]
                    first_data["direction"] = n_related_data["direction"]
                    out_array = []
                    for header in self.out_header_array:
                        out_array.append(first_data[header])
                    return out_array
                else:
                    return None
            else:
                if self.count < self.data_drop_rate:
                    self.count += 1
                else:
                    self.count = 0
                return None

    def set_config(self, new_config):
        if type(new_config) is not dict:
            raise ValueError("The new config input must be dictionary type.")
        try:
            new_filter_config = new_config["filters"]
        except KeyError:
            raise KeyError("The config info does not contain filter info.")
        self.config = new_config
        self.filter_config = new_filter_config

    def set_buffer(self, new_buffer_length):
        if type(new_buffer_length) is not int:
            raise ValueError("The new buffer length input must be integer type.")
        self.circular_buffer = collections.deque(maxlen=new_buffer_length)
        self.buffer_max_length = new_buffer_length

    def set_header_array(self, new_header_array):
        if type(new_header_array) is not list:
            raise ValueError("The header array input must be list type.")
        if not new_header_array:
            raise ValueError("The header array input must not be empty.")
        for header in new_header_array:
            if type(header) is not str:
                raise ValueError("The header_array element must be string.")
        self.header_array = new_header_array
        self.out_header_array = get_out_header_array(new_header_array, self.filter_config)

    def set_drop_rate(self, new_drop_rate):
        if type(new_drop_rate) is not int:
            raise ValueError("The drop rate input must be integer type.")

        self.data_drop_rate = new_drop_rate

    def get_output_header_array(self):
        return self.out_header_array
