# Imports.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from .. import Global_Utilities as gu

# Function definitions.

def plot_data( directory, output_directory, file_data, data, first_derivative_data, second_derivative_data, savefig = False ):

    resin_data = gu.get_list_of_resins_data( directory )

    # For overall pipeline figure.

    # mpl.rcParams['lines.linewidth'] = 4

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    samples_to_plot = [11, 14, 10, 13, 12, 15, 1, 2, 3, 6, 7, 9, 5]
    # samples_to_plot = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8]
    # samples_to_plot = [18, 20, 21, 22, 23]
    # samples_to_plot = [16, 17, 19, 24]
    # samples_to_plot = [11, 14, 10, 13, 4]
    # samples_to_plot = [2, 3, 1, 15, 12, 6, 5, 7, 9, 8, 17, 24, 18, 20, 21, 22, 23]

    specimens = True
    all_specimens = True
    specimen_mask = [0]

    mean = False

    deriv0 = True
    deriv1 = False
    deriv2 = False

    split = False
    num_splits = 2
    split_length = 120
    splits = [split_length * (i + 30 / 120) for i in range( num_splits )]
    # splits = [78, 82]

    log_graph = False

    radial_graph = True

    x, y = 1, 2

    if not split:

        splits = [int( data[1][len( data[1] ) - 1] ), int( data[1][0] )]

    colours = gu.list_of_colours()

    data_extraction = False

    for s in range( len( splits ) - 1 ):

        data_extraction = []

        lower_bound, upper_bound = splits[s], splits[s + 1]

        if radial_graph:

            ax = plt.subplots( 1, 1, subplot_kw = dict( polar = True ) )[1]

            for i in samples_to_plot:

                index = np.where( samples_present_array == i )[0][0]

                freq_mask = np.where( (np.array( data[1] ) <= upper_bound) & (np.array( data[1] ) >= lower_bound) )[0]

                # plt.scatter( np.array( data[10][index] )[freq_mask], np.array( data[11][index] )[freq_mask] )

                alpha_scale = np.linspace( 0.3, 1, len( np.array( data[12][index] )[freq_mask] ) )

                ax.scatter( np.arctan( np.array( data[12][index] )[freq_mask] ), np.array( data[9][index] )[freq_mask], label = resin_data.loc[i]["Label"], color = colours[i], alpha = alpha_scale, s = 100 )

                # ax = plt.gca()
                # ax.set_aspect( 'equal' )

            ax.set_rlim( 3, 150000 )
            ax.set_thetamin( 30 )
            ax.set_thetamax( 75 )
            ax.set_rscale( 'symlog' )

            r = np.arange( 0, 150000, 10 )
            theta = [np.pi / 4 for i in r]
            ax.plot( theta, r, "k--" )

        else:

            for i in samples_to_plot:

                if specimens:

                    mask = np.where( sample_array == i )[0]

                    for ind, j in enumerate( mask ):

                        if (ind in specimen_mask) or all_specimens:

                            if deriv0:

                                freq_mask = np.where( (np.array( data[1] ) <= upper_bound) & (np.array( data[1] ) >= lower_bound) )[0]

                                plt.plot( np.array( data[1] )[freq_mask], np.array( data[y][j] )[freq_mask], label = file_data[j][2], color = colours[i], linewidth = 2.5 )

                                # plt.plot( np.array( data[1] )[freq_mask], np.array( data[3][j] )[freq_mask], label = "Storage Modulus", color = colours[i] )
                                # plt.plot( np.array( data[1] )[freq_mask], np.array( data[4][j] )[freq_mask], label = "Loss Modulus", color = colours[i + 1] )

                                # m = (np.log( data[2][j][3] ) - np.log( data[2][j][1] )) / (np.log( data[1][3] ) - np.log( data[1][1] ))
                                # b = np.log( data[2][j][2] / data[1][2] ** m )

                                data_extraction.append( np.array( data[1] )[freq_mask] )
                                data_extraction.append( np.array( data[3][j] )[freq_mask] )
                                data_extraction.append( np.array( data[4][j] )[freq_mask] )

                                # plt.plot( np.array( data[1] )[freq_mask], np.array( data[1] )[freq_mask] ** m * np.exp( b ), "--", color = colours[i], linewidth = 2.5 )

                            if deriv1:

                                freq_mask = np.where( (np.array( first_derivative_data[1] ) <= upper_bound) & (np.array( first_derivative_data[1] ) >= lower_bound) )[0]

                                # Minus sign for log graph!

                                plt.plot( np.array( first_derivative_data[1] )[freq_mask], -np.array( first_derivative_data[2][j] )[freq_mask], label = file_data[j][2], color = colours[i] )

                            if deriv2:

                                freq_mask = np.where( (np.array( second_derivative_data[1] ) <= upper_bound) & (np.array( second_derivative_data[1] ) >= lower_bound) )[0]

                                plt.plot( np.array( second_derivative_data[1] )[freq_mask], np.array( second_derivative_data[2][j] )[freq_mask], label = file_data[j][2], color = colours[i] )

                if mean:

                    index = np.where( samples_present_array == i )[0][0]

                    if deriv0:

                        freq_mask = np.where( (np.array( data[1] ) <= upper_bound) & (np.array( data[1] ) >= lower_bound) )[0]

                        plt.plot( np.array( data[1] )[freq_mask], np.array( data[9][index] )[freq_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                    if deriv1:

                        freq_mask = np.where( (np.array( first_derivative_data[1] ) <= upper_bound) & (np.array( first_derivative_data[1] ) >= lower_bound) )[0]

                        plt.plot( np.array( first_derivative_data[1] )[freq_mask], np.array( first_derivative_data[9][index] )[freq_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

                    if deriv2:

                        freq_mask = np.where( (np.array( second_derivative_data[1] ) <= upper_bound) & (np.array( second_derivative_data[1] ) >= lower_bound) )[0]

                        plt.plot( np.array( second_derivative_data[1] )[freq_mask], np.array( second_derivative_data[9][index] )[freq_mask], label = resin_data.loc[i]["Label"], color = colours[i] )

        if log_graph:

            ax = plt.gca()
            ax.set_xscale( 'log' )
            ax.set_yscale( 'log' )

        plt.legend( ncol = 2, bbox_to_anchor = ( 1.05, 1 ), loc = 'center', borderaxespad = 0 )
        leg = ax.get_legend()

        # for lh in leg.legendHandles:
        #
        #     lh.set_alpha(1)

        # plt.legend( ncol = 2, loc = 'upper right', borderaxespad = 0 )
        # plt.legend()

        # plt.xlabel( "Angular Frequency" )
        # plt.ylabel( "Complex Viscosity" )

        plt.tight_layout()

        # For overall pipeline figure.

        # ax = plt.gca()
        # ax.get_legend().remove()
        # plt.xlabel( "" )
        # plt.ylabel( "" )
        # plt.tick_params( axis = 'x', which = 'both', bottom = False, top = False, labelbottom = False )
        # plt.tick_params( axis = 'y', which = 'both', left = False, right = False, labelleft = False )

        if savefig:

            plt.savefig( output_directory + "Rheology/Plots/Plot.pdf" )

        else:

            plt.show()

        plt.close()

        if data_extraction:

            array = data_extraction[0][:, np.newaxis]

            for i in range( 1, len( data_extraction ) ):

                array = np.hstack( (array, data_extraction[i][:, np.newaxis]) )

            np.savetxt( output_directory + "Plot_Coords/Unnamed.txt", array )
