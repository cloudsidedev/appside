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

namespace AppFlow\Command;

// use Symfony\Component\Console\Command\Command;
// use Symfony\Component\Console\Input\InputInterface;
// use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Config\Loader\FileLoader;
use Symfony\Component\Yaml\Yaml;

/**
* @author Ivo Marino <ivo.marino@ttss.ch>
*/
class ConfigSourceRC extends FileLoader
{
   public function load($resource, $type = null)
   {
       $configValues = Yaml::parse(file_get_contents($resource));

       // ... handle the config values

       // maybe import some other resource:

       // $this->import('extra_users.yml');
   }

   public function supports($resource, $type = null)
   {
       return is_string($resource) && 'yml' === pathinfo(
           $resource,
           PATHINFO_EXTENSION
       );
   }
}
