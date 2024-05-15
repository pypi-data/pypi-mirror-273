# Imports.

import os
import glob
import re
import numpy as np
import pandas as pd

from .. import Global_Utilities as gu

# Function definitions.

def read_raw_data_file_1( filename, f, resin_data, file_data, data ):

    pattern = re.compile( r"^Resin(\d+)_(\d+)_" )

    resin = int( pattern.search( f ).groups()[0] )

    specimen = int( pattern.search( f ).groups()[1] )

    with open( filename, 'r', encoding = 'utf-16' ) as file:

        column_data = [[] for i in range( 9 )]

        lines = file.readlines()

        linenumber = 0

        for line in lines:

            if linenumber < 10:

                linenumber += 1
                continue

            a_list = line.split()

            column_data[0].append( int( a_list[0] ) )
            column_data[1].append( float( a_list[1] ) )
            column_data[2].append( float( a_list[2] ) )
            column_data[3].append( float( a_list[3] ) )
            column_data[4].append( float( a_list[4] ) )
            column_data[5].append( float( a_list[5] ) )
            column_data[6].append( float( a_list[6] ) )
            column_data[7].append( float( a_list[7] ) )
            column_data[8].append( float( a_list[8] ) )

    for i in range( 9 ):

        data[i].append( column_data[i] )

    file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

def read_raw_data_file_2( filename, f, resin_data, file_data, data ):

    pattern = re.compile( r"^Resin(\d+)_(\d+)_" )

    resin = int( pattern.search( f ).groups()[0] )

    specimen = int( pattern.search( f ).groups()[1] )

    with open( filename, 'r', encoding = "windows-1252" ) as file:

        column_data = [[] for i in range( 10 )]

        lines = file.readlines()

        linenumber = 0

        for line in lines:

            if linenumber < 2:

                linenumber += 1
                continue

            a_list = line.rstrip().split( "," )

            column_data[1].append( float( a_list[3] ) )
            column_data[2].append( float( a_list[9] ) )
            column_data[3].append( float( a_list[0] ) * 10 ** 6 )
            column_data[4].append( float( a_list[1] ) * 10 ** 6 )
            column_data[5].append( float( a_list[1] ) / float( a_list[0] ) )

    for i in range( 9 ):

        column_data[i].reverse()
        data[i].append( column_data[i] )

    file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

def extract_raw_data( directory, data_directory ):
    '''Extract the raw data from the files.'''

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    resins = sorted( [os.path.basename( path ) for path in glob.glob( data_directory + "*" )], key = gu.sort_raw_files_1 )

    file_data, data = [], [[], [], [], [], [], [], [], [], []]

    pattern = re.compile( r"^Resin(\d+)" )

    for r in resins:

        filenames = sorted( [os.path.basename( path ) for path in glob.glob( data_directory + r + "/*" )], key = gu.sort_raw_files_2 )

        resin = int( pattern.search( r ).groups()[0] )

        for f in filenames:

            if resin == 40 or resin == 41:

                read_raw_data_file_2( data_directory + r + "/" + f, f, resin_data, file_data, data )

            else:

                read_raw_data_file_1( data_directory + r + "/" + f, f, resin_data, file_data, data )

    return file_data, data

def standardise_data( data ):
    '''Standardise data.'''

    standardised_angular_frequency = [10 ** (i / 10) for i in range( -10, 21 )]
    standardised_angular_frequency.reverse()

    for i in range( len ( data[1] ) ):

        sample_data = [[], [], [], [], [], [], [], [], []]

        for j in standardised_angular_frequency:

            index_1, index_2 = -2, -1

            for k, v in enumerate( data[1][i] ):

                if v < j:

                    index_1 = k - 1
                    index_2 = k
                    break

            log_change = (np.log10( j ) - np.log10( data[1][i][index_1] )) / (np.log10( data[1][i][index_2] ) - np.log10( data[1][i][index_1] ))

            for l in range( 1, 9 ):

                if data[l][i]:

                    sample_data[l].append( 10 ** ((np.log10( data[l][i][index_2] ) - np.log10( data[l][i][index_1] )) * log_change + np.log10( data[l][i][index_1] )) )

        for l in range( 2, 9 ):

            data[l][i] = sample_data[l]

    data[0] = [i for i in range( 31 )]
    data[1] = standardised_angular_frequency

def add_description_to_file_data( file_data ):
    '''Add descriptions in the form of letters to each specimen.'''

    pass

def read_files_and_preprocess( directory, data_directory, merge_groups ):
    '''Read files and preprocess data.'''

    file_data, data = extract_raw_data( directory, data_directory )

    standardise_data( data )

    add_description_to_file_data( file_data )

    if merge_groups:

        gu.merge( file_data )

    return file_data, data

def write_csv( output_directory, file_data, data ):
    '''Write read and preprocessed data to a .csv file.'''

    for i, f in enumerate( file_data ):

        array = np.array( data[0] )[:, np.newaxis]

        for j in range( 1, 9 ):

            if j == 1:

                array = np.hstack( (array, np.array( data[j] )[:, np.newaxis]) )

            elif data[j][i]:

                array = np.hstack( (array, np.array( data[j][i] )[:, np.newaxis]) )

            else:

                array = np.hstack( (array, np.zeros( len( data[0] ) )[:, np.newaxis]) )

        np.savetxt( output_directory + "Rheology/Condensed_Data/Resin{}_{}_.csv".format( f[0], f[1] ), array, delimiter = "," )

    array = np.array( file_data )

    np.savetxt( output_directory + "Rheology/File_Data/file_data.csv", array, delimiter = ",", fmt = "%s" )

def read_csv( directory, output_directory, merge_groups ):
    '''Read the preprocessed .csv files.'''

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    file_data = []

    df = pd.read_csv( output_directory + "Rheology/File_Data/file_data.csv", sep = ",", header = None )

    for i in range( len( df.index ) ):

        resin = df.iloc[i, 0]
        specimen = df.iloc[i, 1]

        file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

    data = [[], [], [], [], [], [], [], [], []]

    filenames = sorted( [os.path.basename( path ) for path in glob.glob( output_directory + "Rheology/Condensed_Data/*" )], key = gu.sort_raw_files_3 )

    for f in filenames:

        df = pd.read_csv( output_directory + "Rheology/Condensed_Data/" + f, sep = ",", header = None )

        for i in range( len( df.columns ) ):

            data[i].append( df.iloc[:, i].tolist() )

    data[0] = data[0][0]
    data[1] = data[1][0]

    add_description_to_file_data( file_data )

    if merge_groups:

        gu.merge( file_data )

    return file_data, data

def remove_files( file_data, data ):
    '''Remove files not needed/wanted for analysis by searching for letters in file descriptions.'''

    files_to_remove = []

    for i in range( len( file_data ) ):

        if file_data[i][0] == 0:

            pass
            # files_to_remove.append( i )

    files_to_remove.reverse()

    for r in files_to_remove:

        file_data.pop( r )

        for i in range( len ( data ) ):

            if i <= 1:

                continue

            data[i].pop( r )

def compute_mean( output_directory, file_data, data ):
    '''Compute the mean data for each resin.'''

    m = [gu.sample_mean( file_data, data[2] ), gu.sample_mean( file_data, data[3] ), gu.sample_mean( file_data, data[4] ), gu.sample_mean( file_data, data[5] )]

    labels = ["CV", "SM", "LM", "LF"]

    for i in range( len( m ) ):

        array = m[i][0][:, np.newaxis]

        for j in range( 1, len( m[i] ) ):

            array = np.hstack( (array, m[i][j][:, np.newaxis]) )

        np.savetxt( output_directory + "Rheology/Mean_Data/" + labels[i] + "_Means.csv", array, delimiter = "," )

def read_mean( output_directory, data ):
    '''Read the computed means for each resin from a file.'''

    labels = ["CV", "SM", "LM", "LF"]

    for i in range( len( labels ) ):

        m = []

        df = pd.read_csv( output_directory + "Rheology/Mean_Data/" + labels[i] + "_Means.csv", sep = ",", header = None )

        for j in range( len( df.columns ) ):

            m.append( df.iloc[:, j].tolist() )

        data.append( m )
