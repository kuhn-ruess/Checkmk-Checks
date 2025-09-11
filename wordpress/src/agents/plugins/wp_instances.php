#!/usr/bin/env php
<?php
/*
  Copyright 2023 - Stefan Mikuszeit <stefan.mikuszeit@syzygy.de>
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
*/

ini_set('memory_limit', '100M');

$update_core    = array();
$update_plugins = array();
$update_themes  = array();
$arr_output = array();
$wp_instance_info = "";
$GlobalStatus = 0;
$perfdata = "";
$long_output = "";
$default_output_text = "WordPress Status";
$output_errors = "";

function get_cfg_vars() {
    $cfg = array('BASEDIR' => '/var/www', 'SEARCH_STRING' => '/wp/wp-load.php');
    if (file_exists('/etc/check_mk/wp_instances.cfg')) {
        $lines = file('/etc/check_mk/wp_instances.cfg');
        foreach ($lines as $line) {
            if (preg_match('/^\s*BASEDIR\s*=\s*([\S]+)/', $line, $m)) {
                $cfg['BASEDIR'] = $m[1];
            }
            if (preg_match('/^\s*SEARCH_STRING\s*=\s*([\S]+)/', $line, $m)) {
                $cfg['SEARCH_STRING'] = $m[1];
            }
        }
    }
    return $cfg;
}

function find_wp_instances($basedir, $search_string) {
    $cmd = "locate '" . escapeshellcmd($search_string) . "' | grep '" . escapeshellcmd($basedir) . "' | grep -v 'release'";
    exec($cmd, $output, $ret);
    return $output;
}

if ($argc == 1) {
    $cfg = get_cfg_vars();
    $wp_instances = find_wp_instances($cfg['BASEDIR'], $cfg['SEARCH_STRING']);
    $result = array();
    foreach ($wp_instances as $wp_instance_path) {
        $wp_orig_dest = trim(shell_exec('readlink -f ' . escapeshellarg($wp_instance_path)));
        if ($wp_orig_dest && file_exists($wp_orig_dest)) {
            $wp_instance_name = explode('/', $wp_orig_dest);
            $wp_instance_name = isset($wp_instance_name[4]) ? $wp_instance_name[4] : basename($wp_orig_dest);
            $wp_load_directory = dirname($wp_orig_dest);
            ob_start();
            $GLOBALS['wp_instance_name'] = $wp_instance_name;
            get_wp_instance_infos($wp_load_directory);
            $json = ob_get_clean();
            $json = rtrim($json, ",");
            if ($json) {
                $result[] = $json;
            }
        }
    }
    echo "{\"instances\": [" . implode(',', $result) . "]}" . PHP_EOL;
    exit;
} elseif ($argc == 3) {
    $wp_directory = $argv[1];
    $wp_instance_name = $argv[2];
    if (is_dir($wp_directory)) {
        $GLOBALS['wp_instance_name'] = $wp_instance_name;
        get_wp_instance_infos($wp_directory);
        exit;
    } else {
        echo "Base Directory doesn't exist" . PHP_EOL;
        exit(3);
    }
} else {
    echo "Usage: php " . basename(__FILE__) . " [Full path to wp-load.php] [WP Instance]" . PHP_EOL;
    exit;
}

function syzygy_json_ErrorHandler($errno, $errstr, $errfile, $errline){
    $errstr=htmlentities($errstr, ENT_QUOTES);
    return true;
    switch ($errno) {
        case E_USER_ERROR:
	    echo json_encode(['errno' => $errno, 'error' => $errstr, 'errfile' => $errfile, 'errline' => $errline]).",";
            exit(1);

        case E_USER_WARNING:
            echo json_encode(['errno' => $errno, 'error' => $errstr, 'errfile' => $errfile, 'errline' => $errline]).",";
            break;

        case E_USER_NOTICE:
            echo json_encode(['errno' => $errno, 'error' => $errstr, 'errfile' => $errfile, 'errline' => $errline]).",";
            break;

        default:
            echo json_encode(['errno' => $errno, 'error' => $errstr, 'errfile' => $errfile, 'errline' => $errline]).",";
            break;
    }
    /* Don't execute PHP internal error handler */
    return true;
}

function get_wp_instance_infos($wp_directory){
    set_error_handler("syzygy_json_ErrorHandler");
    chdir($wp_directory);
    try{
        require($wp_directory."/wp-load.php");
    }catch(Throwable $e){
	echo "";
    	// var_dump($e);
	// echo "{'errno':'".$e->errno."','error':'".$e->errstr."','file':'".$e->errfile."','line':'".$e->errline."'},";
	// echo json_encode(['errno' => $e->getCode(), 'error' => $e->getMessage(), 'errfile' => $e->getFile(), 'errline' => $e->getLine()]).",";
	# echo 'And my error is: ' . $e->getMessage();
    }
    GLOBAL $wp_version;
    GLOBAL $wp_instance_name;

    try{
    	wp_update_plugins();
    }catch(Throwable $e){
        echo "";
        // var_dump($e);
        // echo "{'errno':'".$e->errno."','error':'".$e->errstr."','file':'".$e->errfile."','line':'".$e->errline."'},";
        //echo json_encode(['errno' => $e->getCode(), 'error' => $e->getMessage(), 'errfile' => $e->getFile(), 'errline' => $e->getLine()]).",";
        # echo 'And my error is: ' . $e->getMessage();
    }

    @wp_version_check();
    @wp_update_themes();
    restore_error_handler();
    $core = @get_site_transient('update_core');
    $plugins = @get_site_transient('update_plugins');
    $themes = @get_site_transient('update_themes');

    if ($themes && $themes !== null) {
	$update_themes=@get_wp_themes_infos($themes);
    }

    if ($plugins && $plugins !== null) {
        $update_plugins=@get_wp_plugins_infos($plugins);
    }

    if ($core && $core !== null) {
	$update_core=@get_wp_core_infos($core);
    }

    if ( $update_core || $update_plugins || $update_themes) {
        generate_output($update_core,$update_plugins,$update_themes);
    } else {
        if ($wp_version < 3 ) {
            $arr_output['error']="Wordpress Version < 3 - Check Script does not work - Upgrade ASAP!";
            die(json_encode($arr_output).",");
	}
	$arr_output['name']=$wp_instance_name;
	$arr_output['core_status']=0;
        $arr_output['core_version']=$wp_version;
        $arr_output['core_new_version']="";
        die(json_encode($arr_output).",");
    }
}

function get_wp_themes_infos($themes){
    GLOBAL $update_themes;
    $arr_theme_updates=array();
    $i=0;
    if(is_array($themes->translations) && count($themes->translations)>0){
        $arr_themes_translations = json_decode(json_encode($themes->translations), true);
        foreach($arr_themes_translations as $installed_theme){
            $installed_theme_name=strval($installed_theme['slug']);
            $installed_theme_version=strval($installed_theme['version']);
	    $arr_theme_updates[$installed_theme_name]['version']=$installed_theme_version;
            if(is_array($themes->response) && count($themes->response)>0){
                $arr_themes_response = json_decode(json_encode($themes->response), true);
		foreach($arr_themes_response as $theme) {
                    $arr_theme_updates[$theme['theme']]['new_version']=$theme['new_version'];
                    $arr_theme_updates[$theme['theme']]['status']=1;
                }
            }
            if(!isset($arr_theme_updates[$installed_theme_name]['new_version'])){
                $arr_theme_updates[$installed_theme_name]['new_version']="";
                $arr_theme_updates[$installed_theme_name]['status']=0;
            }
        }
    }else{
        // No Themes Installed
        $arr_theme_updates=Array();
    }
    // echo "arr_theme_updates: ".var_dump($arr_theme_updates);
    return $arr_theme_updates;
}

function get_wp_plugins_infos($plugins){
    GLOBAL $update_plugins;
    $arr_plugin_updates=array();
    if(is_array($plugins->translations) && count($plugins->translations)>0){
        $arr_plugins_translations = json_decode(json_encode($plugins->translations), true);
	// var_dump($arr_plugins_translations);
        foreach($arr_plugins_translations as $installed_plugin){
            $installed_plugin_name=strval($installed_plugin['slug']);
            $installed_plugin_version=strval($installed_plugin['version']);
	    $installed_plugin_language=strval($installed_plugin['language']);
            $arr_plugin_updates[$installed_plugin_name]['version']=$installed_plugin_version;
            if(is_array($plugins->response) && count($plugins->response)>0){
                $arr_plugin_response = json_decode(json_encode($plugins->response), true);
		// var_dump($arr_plugin_response);
                foreach($arr_plugin_response as $plugin){
                    $arr_plugin_updates[$plugin['slug']]['new_version']=$plugin['new_version'];
                    $arr_plugin_updates[$plugin['slug']]['status']=1;
                }
            }
	    if(!isset($arr_plugin_updates[$installed_plugin_name]['new_version'])){
		$arr_plugin_updates[$installed_plugin_name]['new_version']="";
	        $arr_plugin_updates[$installed_plugin_name]['status']=0;
	    }
        }
    }else{
        // No Plugins installed
        $arr_plugin_updates=array();
    }
    return $arr_plugin_updates;
}

function get_wp_core_infos($core){
    GLOBAL $update_core;
    $arr_core = @$core->updates;
    if (is_array($arr_core) && $arr_core[0]) {
        $obj_core = $arr_core[0];
        if ($obj_core->response && $obj_core->response != "latest") {
            $update_core = $obj_core->current;
        }
    }
    return $update_core;
}

function generate_output($update_core,$update_plugins,$update_themes){
    /*
        print "Installed WP Version: $wp_version\n";
        print "Core: $update_core\n";
        print "Plugins: " . join($update_plugins,',') . "\n";
        print "Themes: " . join($update_themes,',') . "\n";
     */

    global $wp_version;
    global $wp_instance_name;
    global $arr_output;

    $status="";
    #$arr_output["instance"]["$wp_instance_name"]=Array();
    $arr_output["name"]=$wp_instance_name;
    if ($update_core) {
	$core_status=0;
	if(isset($wp_version)){
		@list($major, $minor, $patch) = explode('.', $wp_version);
		@list($update_major, $update_minor, $update_patch) = explode('.', $update_core);
		if(
			isset($major) && is_numeric($major) && 
			isset($minor) && is_numeric($minor) && 
			isset($patch) && is_numeric($patch) &&
                        isset($update_major) && is_numeric($update_major) && 
                        isset($update_minor) && is_numeric($update_minor) && 
                        isset($update_patch) && is_numeric($update_patch)
		){
			if(($update_major > $major) OR ($update_minor > $minor)){
				$core_status=2;
			}
			if($update_patch > $patch){
				if($core_status < 1){
					$core_status=1;
				}
			}
		}
	}else{
		$core_status=2;
	}
	$arr_output["core_status"] = $core_status;
	$arr_output["core_version"] = $wp_version;
	$arr_output["core_new_version"] = $update_core;
    } else {
	$arr_output["core_status"] = 0;
        $arr_output["core_version"] = $wp_version;
        $arr_output["core_new_version"] = "";
    }

    if (isset($update_plugins) && is_array($update_plugins) && count($update_plugins) > 0 ) {
	$i=0;
        foreach($update_plugins AS $key => $value){
            if(isset($value['version'])){
		$arr_output['plugins'][$i]['name']=$key;
                $arr_output['plugins'][$i]['version']=$value['version'];
		$arr_output['plugins'][$i]['new_version']=$value['new_version'];
		$arr_output['plugins'][$i]['status']=$value['status'];
		$i++;
	    }
        }
#    } else {
#        $arr_output["instance"][$wp_instance_name]['plugin']['status']=0;
    }

    # $message .= " - ";

    if (isset($update_themes) && is_array($update_themes) && count($update_themes) > 0) {
	$i=0;
        foreach($update_themes AS $key => $value){
	    if(isset($value['version'])){
		$arr_output["themes"][$i]['name']=$key;
                $arr_output["themes"][$i]['version']=$value['version'];
		$arr_output["themes"][$i]['new_version']=$value['new_version'];
		$arr_output["themes"][$i]['status']=$value['status'];
		$i++;
            }
        }
#    } else {
#	$arr_output["instance"][$wp_instance_name]['theme']['status']=0;
    }

    die(json_encode($arr_output).",");
}

?>


