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

use Symfony\Component\Config\Definition\ConfigurationInterface;
use Symfony\Component\Config\Definition\Builder\TreeBuilder;

class Configuration implements ConfigurationInterface
{
    public function getConfigTreeBuilder()
    {
        $treeBuilder = new TreeBuilder();
        $rootNode = $treeBuilder->root('appflow');

        $rootNode
            ->children()
                ->arrayNode('tenant')
                    ->children()
                      ->scalarNode('id')->end()
                      ->scalarNode('name')->end()
                      ->scalarNode('default_env')->end()
                    ->end()
                ->end()
            ->end()
        ;

        return $treeBuilder;
    }
}
