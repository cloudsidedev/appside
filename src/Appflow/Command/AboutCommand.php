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

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;

/**
 * @author Ivo Marino <ivo.marino@ttss.ch>
 */
class AboutCommand extends Command
{
    protected function configure()
    {
        $this
            ->setName('about')
            ->setDescription('Short information about AppFlow')
            ->setHelp(<<<EOT
<info>appflow about</info>
EOT
            )
        ;
    }
    protected function execute(InputInterface $input, OutputInterface $output)
    {
        $output->write(<<<EOT
<info>AppFlow - Multitenant environment automation</info>
<comment>AppFlow is a fully automated multitenant provisiong tool for different environments.
See http://appflow.sh/ for more information.</comment>

EOT
        );
    }
}
