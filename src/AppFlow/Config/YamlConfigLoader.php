<?php

/*
 * This file is part of AppFlow.
 *
 * (c) Ivo Marino <ivo.marino@ttss.ch>
 *     Luca Di Maio <luca.dimaio@ttss.ch>
 *
 * For the full copyright and license information, please view the LICENSE
 * file that was distributed with this source code.
 */

namespace AppFlow\Config;

use Symfony\Component\Config\Loader\FileLoader;
use Symfony\Component\Yaml\Yaml;

/**
* @author Ivo Marino <ivo.marino@ttss.ch>
*/
class YamlConfigLoader extends FileLoader
{
   public function load($resource, $type = null)
   {
       $configValues = Yaml::parse(file_get_contents($resource));

       return $configValues;
   }

   public function supports($resource, $type = null)
   {
       return is_string($resource) && 'yml' === pathinfo(
           $resource,
           PATHINFO_EXTENSION
       );
   }
}
