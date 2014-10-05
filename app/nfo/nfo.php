<?php

// [AnKoA] Made with love by grm34 (FRIPOUILLEJACK)

// Copyright PARDO Jérémy (Sept 2014)
// Contact: jerem.pardo@gmail.com

// This software is a computer program whose purpose is to help command
// line encoders. Intuitive command line interface with many tools:

// * FFMPEG easy encoding
// * Thumbnails Generator
// * NFO Generator
// * Genprez Upload
// * Auto make .torrent

// This software is governed by the CeCILL-C license under French law and
// abiding by the rules of distribution of free software.  You can  use,
// modify and/or redistribute the software under the terms of the CeCILL-C
// license as circulated by CEA, CNRS and INRIA at the following URL
// "http://www.cecill.info".

// As a counterpart to the access to the source code and  rights to copy,
// modify and redistribute granted by the license, users are provided only
// with a limited warranty  and the software's author,  the holder of the
// economic rights,  and the successive licensors  have only  limited
// liability.

// In this respect, the user's attention is drawn to the risks associated
// with loading,  using,  modifying and/or developing or reproducing the
// software by the user in light of its specific status of free software,
// that may mean  that it is complicated to manipulate,  and  that  also
// therefore means  that it is reserved for developers  and  experienced
// professionals having in-depth computer knowledge. Users are therefore
// encouraged to load and test the software's suitability as regards their
// requirements in conditions enabling the security of their systems and/or
// data to be ensured and,  more generally, to use and operate it in the
// same conditions as regards security.

// The fact that you are presently reading this means that you have had
// knowledge of the CeCILL-C license and that you accept its terms.


# SCAN SOURCE & IMPORT DATA
function get_media_info( $video ){
    $media_infos = array( ); $content = shell_exec( 'mediainfo "' . $video . '"' ); $xx = explode( "\n\n", $content );

    foreach ( $xx as $data ){$infos = explode( "\n", $data ); $media_type = '';
        foreach ( $infos as $key => $val ){@list($k, $v, $e) = explode( ":", $val );
            if ( empty( $v ) ){$media_type = $k;}
            else{
                $media_key = str_replace( array( ' ' ), '_', trim( strtolower( $k ) ) );
                $media_value = trim( $v );
                if ( !empty( $e ) )$media_value .= ":$e"; $media_infos[$media_type][$media_key] = $media_value;
            }
        }
    }return $media_infos;
}

# PARSE SOURCE INFOS
function get_nfo( $video, $release_name, $source, $sourcesrt, $imdb, $forced ){ $media = get_media_info( $video );

    // CODECS AUDIO
    $ACODEC['55'] = 'MP3'; $ACODEC['6B'] = 'MP3'; $ACODEC['A_MPEG/L3'] = 'MP3'; $ACODEC['MP3'] = 'MP3';     # MP3
    $ACODEC['40'] = 'AAC'; $ACODEC['67'] = 'AAC'; $ACODEC['AAC'] = 'AAC'; $ACODEC['A_AAC'] = 'AAC';         # AAC
    $ACODEC['A_AC3'] = 'AC3'; $ACODEC['AC-3'] = 'AC3'; $ACODEC['AC3'] = 'AC3';                              # AC3
    $ACODEC['A_DTS'] = 'DTS'; $ACODEC['DTS'] = 'DTS';                                                       # DTS
    $ACODEC['A_FLAC'] = 'FLAC'; $ACODEC['FLAC'] = 'FLAC';                                                   # FLAC
    $ACODEC['A_TRUEHD'] = 'TrueHD'; $ACODEC['TRUEHD'] = 'TrueHD';                                           # TrueHD
    $ACODEC['N/A'] = 'N/A'; $ACODEC[''] = '';

    // VIDEO INFOS
    if(isset( $media['Video'] )){ $tags['V_R'] = preg_replace('`([^0-9])`i', '', $media['Video']['width'] ) . " x " . preg_replace('`([^0-9])`i', '', $media['Video']['height'] );}
    else{ $tags['V_R'] = '...x...' ;}
    $tags['V_A'] = isset( $media['Video']['display_aspect_ratio'] ) ? $media['Video']['display_aspect_ratio'] : 'N/A';
    $tags['V_L'] = isset( $media['General']['duration'] ) ? $media['General']['duration'] : 'N/A';
    $tags['SIZE'] = isset( $media['General']['file_size'] ) ? $media['General']['file_size'] : 'N/A';
    if(isset( $media['Video']['writing_library'])){$tags['V_C'] = (preg_match('/(\w+\s\w+\s\w+)/i', $media['Video']['writing_library'], $matches))? $matches[0] : 'x264' ;} else{$tags['V_C'] = "x264" ;}
    $tags['V_F'] = isset( $media['Video']['frame_rate'] ) ? $media['Video']['frame_rate'] : 'N/A';
    $tags['V_FP'] = isset( $media['Video']['format_profile'] ) ? $media['Video']['format_profile'] : 'N/A';
    $tags['V_B'] = isset( $media['Video']['bit_rate'] ) ? $media['Video']['bit_rate'] : ( isset( $media['Video']['nominal_bit_rate'] ) ? $media['Video']['nominal_bit_rate'] : isset($media['General']['overall_bit_rate'] ) ? $media['General']['overall_bit_rate'] : 'N/A' );

    // AUDIO 1 INFOS
    $tags['A_L'] = isset( $media['Audio']['title'] ) ? $media['Audio']['title'] : ( isset( $media['Audio #1']['title'] ) ? $media['Audio #1']['title'] : 'ENGLiSH' );
    $A_C = isset( $media['Audio']['codec_id'] ) ? $media['Audio']['codec_id'] : ( isset( $media['Audio #1']['codec_id'] ) ? $media['Audio #1']['codec_id'] : 'N/A' ); $tags['A_C'] = $ACODEC[$A_C];
    $tags['A_B'] = isset( $media['Audio']['bit_rate'] ) ? $media['Audio']['bit_rate'] : ( isset( $media['Audio #1']['bit_rate'] ) ? $media['Audio #1']['bit_rate'] : '128Kbps' );
    $tags['A_SR'] = isset( $media['Audio']['sampling_rate'] ) ? $media['Audio']['sampling_rate'] : ( isset( $media['Audio #1']['sampling_rate'] ) ? $media['Audio #1']['sampling_rate'] : 'N/A' );
    $tags['A_CH'] = isset( $media['Audio']['channel(s)'] ) ? $media['Audio']['channel(s)'] : ( isset( $media['Audio #1']['channel(s)'] ) ? $media['Audio #1']['channel(s)'] : 'N/A' );
    $tags['A_MOD'] = isset( $media['Audio']['compression_mode'] ) ? $media['Audio']['compression_mode'] : ( isset( $media['Audio #1']['compression_mode'] ) ? $media['Audio #1']['compression_mode'] : 'Lossy' );

    // AUDIO 2 INFOS
    $A_L2 = isset( $media['Audio #2']['title'] ) ? $media['Audio #2']['title'] : '';
    $A_C2 = isset( $media['Audio #2']['codec_id'] ) ? $media['Audio #2']['codec_id'] : ''; $tags['A_C2'] = $ACODEC[$A_C2];
    $A_B2 = isset( $media['Audio #2']['bit_rate'] ) ? $media['Audio #2']['bit_rate'] : '';
    $A_SR2 = isset( $media['Audio #2']['sampling_rate'] ) ? $media['Audio #2']['sampling_rate'] : '';
    $A_CH2 = isset( $media['Audio #2']['channel(s)'] ) ? $media['Audio #2']['channel(s)'] : '';
    $A_MOD2 = isset( $media['Audio #2']['compression_mode'] ) ? $media['Audio #2']['compression_mode'] : '';
    if(isset( $media['Audio #2'] )){ $tags['A_L2'] = '|  '.$A_L2; $tags['A_C2'] = '|  '.$tags['A_C2']; $tags['A_B2'] = '|  '.$A_B2; $tags['A_SR2'] = '|  '.$A_SR2; $tags['A_CH2'] = '|  '.$A_CH2; $tags['A_MOD2'] = '|  '.$A_MOD2;}
    else{ $tags['A_L2'] = $A_L2; $tags['A_C2'] = $tags['A_C2']; $tags['A_B2'] = $A_B2; $tags['A_SR2'] = $A_SR2; $tags['A_CH2'] = $A_CH2; $tags['A_MOD2'] = $A_MOD2;}

    // SUBTITLES INFOS
    $tags['S_F'] = isset( $media['Text']['format'] ) ? $media['Text']['format'] : ( isset( $media['Text #1']['format'] ) ? $media['Text #1']['format'] : 'N/A' );
    $tags['S_C'] = isset( $media['Text']['codec_id'] ) ? $media['Text']['codec_id'] : ( isset( $media['Text #1']['codec_id'] ) ? $media['Text #1']['codec_id'] : 'N/A' );

    // RELEASE INFOS
    $tags['DATE'] = @date( 'd-m-Y' ); $tags['SOURCE'] = $source; $tags['SOURCESRT'] = $sourcesrt; $tags['B0'] = $imdb; $tags['TITRE_RELEASE'] = $release_name; $tags['FORCED'] = $forced;

    // WRITE NFO
    $template = file_get_contents( "user/nfo_base.nfo" ); preg_match_all( "/<\!(.*?)[ ]*\!>/", $template, $matches );
    foreach ( $matches[1] as $key => $value ){$template_value = $tags[$value]; $taglen = strlen( $matches[0][$key] ); $align = STR_PAD_RIGHT;
        if ( in_array( $value, array( 'TITRE_RELEASE' ) ) ) $align = STR_PAD_BOTH; $template = str_replace( $matches[0][$key], str_pad( substr( $template_value, 0, $taglen ), $taglen, ' ', $align ), $template );
    }return $template; }

# FINALLY
$new_template = get_nfo( $_SERVER['argv'][1], $_SERVER['argv'][2], $_SERVER['argv'][3], $_SERVER['argv'][4], $_SERVER['argv'][5], $_SERVER['argv'][6] ); echo $new_template . "\n\n";

?>
